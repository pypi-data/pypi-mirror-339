# Model: feature_space_proximity
#
# Description: The feature_space_proximity model computes nearest neighbors for the given feature space
#

# Template Placeholders
TEMPLATE_PARAMS = {
    "id_column": "udm_mol_bat_id",
    "features": ['mollogp', 'tpsa', 'peoe_vsa6', 'nbase', 'fr_sulfone', 'fr_bicyclic', 'bcut2d_mrhi', 'minpartialcharge', 'estate_vsa1', 'nacid', 'peoe_vsa1', 'fr_aniline', 'minestateindex', 'fr_coo2', 'slogp_vsa4', 'fr_sulfonamd', 'peoe_vsa11', 'fr_c_o_nocoo', 'bcut2d_mrlow', 'bcut2d_logplow', 'vsa_estate3', 'peoe_vsa8', 'numaliphaticcarbocycles', 'bcut2d_mwhi', 'fr_ar_coo', 'slogp_vsa10', 'fr_ar_n', 'kappa3', 'nhohcount', 'slogp_vsa1', 'vsa_estate9', 'maxabspartialcharge', 'vsa_estate5', 'peoe_vsa2', 'smr_vsa3', 'estate_vsa3', 'peoe_vsa7', 'kappa2', 'peoe_vsa10', 'vsa_estate2', 'vsa_estate7', 'bcut2d_mwlow', 'smr_vsa5', 'bcut2d_logphi', 'chi2v', 'peoe_vsa13', 'fr_imidazole', 'apol', 'fr_ester', 'slogp_vsa11'],
    "target": "udm_asy_res_value"
}

from io import StringIO
import json
import argparse
import os
import pandas as pd

# Local Imports
from proximity import Proximity


# Function to check if dataframe is empty
def check_dataframe(df: pd.DataFrame, df_name: str) -> None:
    """Check if the DataFrame is empty and raise an error if so."""
    if df.empty:
        msg = f"*** The training data {df_name} has 0 rows! ***STOPPING***"
        print(msg)
        raise ValueError(msg)


# Function to match DataFrame columns to model features (case-insensitive)
def match_features_case_insensitive(df: pd.DataFrame, model_features: list) -> pd.DataFrame:
    """Match and rename DataFrame columns to match the model's features, case-insensitively."""
    # Create a set of exact matches from the DataFrame columns
    exact_match_set = set(df.columns)

    # Create a case-insensitive map of DataFrame columns
    column_map = {col.lower(): col for col in df.columns}
    rename_dict = {}

    # Build a dictionary for renaming columns based on case-insensitive matching
    for feature in model_features:
        if feature in exact_match_set:
            rename_dict[feature] = feature
        elif feature.lower() in column_map:
            rename_dict[column_map[feature.lower()]] = feature

    # Rename columns in the DataFrame to match model features
    return df.rename(columns=rename_dict)


# TRAINING SECTION
#
# This section (__main__) is where SageMaker will execute the training job
# and save the model artifacts to the model directory.
#
if __name__ == "__main__":
    # Template Parameters
    id_column = TEMPLATE_PARAMS["id_column"]
    features = TEMPLATE_PARAMS["features"]
    target = TEMPLATE_PARAMS["target"]  # Can be None for unsupervised models

    # Script arguments for input/output directories
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR", "/opt/ml/model"))
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN", "/opt/ml/input/data/train"))
    parser.add_argument(
        "--output-data-dir", type=str, default=os.environ.get("SM_OUTPUT_DATA_DIR", "/opt/ml/output/data")
    )
    args = parser.parse_args()

    # Load training data from the specified directory
    training_files = [
        os.path.join(args.train, file)
        for file in os.listdir(args.train) if file.endswith(".csv")
    ]
    all_df = pd.concat([pd.read_csv(file, engine="python") for file in training_files])

    # Check if the DataFrame is empty
    check_dataframe(all_df, "training_df")

    # Create the Proximity model
    model = Proximity(all_df, id_column, features, target, n_neighbors=5)

    # Now serialize the model
    model.serialize(args.model_dir)

# Model loading and prediction functions
def model_fn(model_dir):

    # Deserialize the model
    model = Proximity.deserialize(model_dir)
    return model


def input_fn(input_data, content_type):
    """Parse input data and return a DataFrame."""
    if not input_data:
        raise ValueError("Empty input data is not supported!")

    # Decode bytes to string if necessary
    if isinstance(input_data, bytes):
        input_data = input_data.decode("utf-8")

    if "text/csv" in content_type:
        return pd.read_csv(StringIO(input_data))
    elif "application/json" in content_type:
        return pd.DataFrame(json.loads(input_data))  # Assumes JSON array of records
    else:
        raise ValueError(f"{content_type} not supported!")


def output_fn(output_df, accept_type):
    """Supports both CSV and JSON output formats."""
    use_explicit_na = False
    if "text/csv" in accept_type:
        if use_explicit_na:
            csv_output = output_df.fillna("N/A").to_csv(index=False)  # CSV with N/A for missing values
        else:
            csv_output = output_df.to_csv(index=False)
        return csv_output, "text/csv"
    elif "application/json" in accept_type:
        return output_df.to_json(orient="records"), "application/json"  # JSON array of records (NaNs -> null)
    else:
        raise RuntimeError(f"{accept_type} accept type is not supported by this script.")


# Prediction function
def predict_fn(df, model):
    # Match column names before prediction if needed
    df = match_features_case_insensitive(df, model.features + [model.id_column])

    # Compute Nearest neighbors
    df = model.neighbors(df)
    return df
