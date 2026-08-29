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
    # SELECT BEST CURRENT MODEL
    # =====================================

    def get_best_model(
        self,
        symbol
    ):

        symbol = symbol.upper()

        models = self.get_models(
            symbol
        )

        if len(models) == 0:

            raise ValueError(
                f"No models available for {symbol}"
            )

        # -------------------------------------
        # Keep only models whose files exist.
        # Registry paths are relative to the
        # backend working directory.
        # -------------------------------------

        valid_models = []

        for model in models:

            model_path = model.get(
                "path",
                ""
            )

            if os.path.exists(
                model_path
            ):

                valid_models.append(
                    model
                )

        if len(valid_models) == 0:

            raise ValueError(
                f"No valid model files found for {symbol}"
            )

        # -------------------------------------
        # Keep only the newest version of each
        # model type.
        #
        # This prevents stale historical models
        # from winning model selection.
        # -------------------------------------

        latest_by_model = {}

        for model in valid_models:

            model_name = model.get(
                "model",
                ""
            )

            version = str(
                model.get(
                    "version",
                    ""
                )
            )

            if (
                model_name not in latest_by_model
                or version > str(
                    latest_by_model[
                        model_name
                    ].get(
                        "version",
                        ""
                    )
                )
            ):

                latest_by_model[
                    model_name
                ] = model

        current_models = list(
            latest_by_model.values()
        )

        if len(current_models) == 0:

            raise ValueError(
                f"No current models available for {symbol}"
            )

        # -------------------------------------
        # Model selection priority:
        #
        # 1. Highest F1
        # 2. Highest accuracy
        # 3. Newest version
        #
        # NaN/invalid metric values are treated
        # as zero.
        # -------------------------------------

        def model_score(model):

            metrics = model.get(
                "metrics",
                {}
            )

            f1 = metrics.get(
                "f1",
                0.0
            )

            accuracy = metrics.get(
                "accuracy",
                0.0
            )

            try:

                f1 = float(f1)

                if not np.isfinite(f1):

                    f1 = 0.0

            except (
                TypeError,
                ValueError
            ):

                f1 = 0.0

            try:

                accuracy = float(
                    accuracy
                )

                if not np.isfinite(
                    accuracy
                ):

                    accuracy = 0.0

            except (
                TypeError,
                ValueError
            ):

                accuracy = 0.0

            return (
                f1,
                accuracy,
                str(
                    model.get(
                        "version",
                        ""
                    )
                )
            )

        best_model = max(
            current_models,
            key=model_score
        )

        # -------------------------------------
        # Log model selection for transparency.
        # -------------------------------------

        print(
            f"Model selection for {symbol}:"
        )

        for model in current_models:

            metrics = model.get(
                "metrics",
                {}
            )

            print(
                f"  {model.get('model')} "
                f"{model.get('version')} "
                f"F1={metrics.get('f1')} "
                f"Accuracy={metrics.get('accuracy')}"
            )

        print(
            f"Selected model: "
            f"{best_model.get('model')} "
            f"{best_model.get('version')}"
        )

        return best_model
