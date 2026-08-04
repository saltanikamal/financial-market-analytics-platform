from app.ml.algorithms.xgboost_model import XGBoostModel
from app.ml.algorithms.random_forest_model import RandomForestModel


class ModelFactory:
    """
    Factory for creating ML classification model wrappers.

    Supported models:
        - xgboost
        - random_forest

    Each model implements:
        train()
        predict()
        evaluate()
        save()
        load()
        get_feature_importance()
    """


    @staticmethod
    def create_model(model_name):

        model_name = model_name.lower()


        # ==========================
        # XGBOOST
        # ==========================

        if model_name == "xgboost":

            return XGBoostModel()



        # ==========================
        # RANDOM FOREST
        # ==========================

        elif model_name == "random_forest":

            return RandomForestModel()



        else:

            raise ValueError(
                f"Unknown model: {model_name}"
            )
