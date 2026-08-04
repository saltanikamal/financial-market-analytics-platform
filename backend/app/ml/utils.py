import joblib


def load_model(model_path):

    """
    Load trained ML model from disk.

    model_path:
        Full path to .pkl file
    """

    model = joblib.load(
        model_path
    )

    return model
