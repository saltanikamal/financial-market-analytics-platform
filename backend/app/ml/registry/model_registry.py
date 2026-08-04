import json
import os

from datetime import datetime

import numpy as np



class ModelRegistry:
    """
    Registry for storing and selecting ML models.

    Supports classification models:

    - XGBoost Classifier
    - Random Forest Classifier


    Model selection priority:

    1. Multiclass compatible models
    2. Highest F1 score
    3. Highest accuracy
    4. Newest version

    """



    def __init__(self):

        self.registry_path = (
            "app/ml/models/registry.json"
        )



    # =====================================
    # JSON SERIALIZATION FIX
    # =====================================

    def make_json_serializable(self, obj):

        """
        Convert NumPy objects into
        standard Python objects for JSON.
        """


        if isinstance(obj, dict):

            return {

                key: self.make_json_serializable(value)

                for key, value in obj.items()

            }


        elif isinstance(obj, list):

            return [

                self.make_json_serializable(item)

                for item in obj

            ]


        elif isinstance(obj, np.integer):

            return int(obj)


        elif isinstance(obj, np.floating):

            return float(obj)


        elif isinstance(obj, np.ndarray):

            return obj.tolist()


        else:

            return obj



    # =====================================
    # LOAD REGISTRY
    # =====================================

    def load_registry(self):

        if not os.path.exists(
            self.registry_path
        ):

            return {}


        with open(
            self.registry_path,
            "r"
        ) as f:

            return json.load(f)



    # =====================================
    # SAVE REGISTRY
    # =====================================

    def save_registry(
        self,
        registry
    ):


        directory = os.path.dirname(
            self.registry_path
        )


        os.makedirs(
            directory,
            exist_ok=True
        )


        registry = self.make_json_serializable(
            registry
        )


        with open(
            self.registry_path,
            "w"
        ) as f:

            json.dump(
                registry,
                f,
                indent=4
            )



    # =====================================
    # REGISTER MODEL
    # =====================================

    def register_model(
        self,
        symbol,
        model_name,
        version,
        model_path,
        metrics,
        features,
        feature_importance=None
    ):


        registry = self.load_registry()


        symbol = symbol.upper()



        # Convert NumPy values

        metrics = self.make_json_serializable(
            metrics
        )


        features = self.make_json_serializable(
            features
        )


        feature_importance = self.make_json_serializable(
            feature_importance
        )



        if symbol not in registry:

            registry[symbol] = []



        registry[symbol].append(

            {

                "model": model_name,


                "version": version,


                "path": model_path,


                "metrics": metrics,


                "features": features,


                "feature_importance": feature_importance,


                "created_at":
                    datetime.now().isoformat()

            }

        )


        self.save_registry(
            registry
        )



    # =====================================
    # GET MODELS
    # =====================================

    def get_models(
        self,
        symbol
    ):


        registry = self.load_registry()


        symbol = symbol.upper()



        if symbol not in registry:

            raise ValueError(
                f"No models registered for {symbol}"
            )



        return registry[symbol]

    # =====================================
    # SELECT BEST MODEL
    # =====================================

    def get_best_model(
        self,
        symbol
    ):

        models = self.get_models(
            symbol
        )


        if len(models) == 0:

            raise ValueError(
                f"No models available for {symbol}"
            )


        # -------------------------------------
        # All current models in this project
        # are multiclass classifiers.
        #
        # Older versions filtered models based
        # on feature count, which was fragile.
        # -------------------------------------

        multiclass_models = models


        best_model = max(

            multiclass_models,

            key=lambda x: (

                x.get(
                    "metrics",
                    {}
                ).get(
                    "f1",
                    0
                ),

                x.get(
                    "metrics",
                    {}
                ).get(
                    "accuracy",
                    0
                ),

                x.get(
                    "version",
                    ""
                )

            )

        )


        return best_model


