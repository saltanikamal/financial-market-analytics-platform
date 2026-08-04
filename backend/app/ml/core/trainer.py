import os
from datetime import datetime

import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from sklearn.model_selection import train_test_split


from app.ml.config import FEATURE_COLUMNS
from app.ml.data_loader import load_stock_data
from app.ml.feature_engineering import FeatureEngineer

from app.ml.core.model_factory import ModelFactory

from app.ml.utils import save_model

from app.ml.registry.model_registry import ModelRegistry



class Trainer:
    """
    Complete ML Training Pipeline

    Responsibilities:

    1. Load stock data
    2. Create features
    3. Prepare training data
    4. Train selected model
    5. Evaluate model
    6. Save model
    7. Register model metadata

    """



    def __init__(
        self,
        symbol: str,
        model_name: str = "xgboost"
    ):

        self.symbol = symbol.upper()

        self.model_name = model_name


        self.model_dir = os.path.join(
            os.path.dirname(
                os.path.dirname(__file__)
            ),
            "models",
            "latest"
        )


        os.makedirs(
            self.model_dir,
            exist_ok=True
        )


        self.registry = ModelRegistry()



    # -------------------------
    # LOAD DATA
    # -------------------------

    def load_data(self):

        return load_stock_data(
            self.symbol
        )



    # -------------------------
    # FEATURE ENGINEERING
    # -------------------------

    def prepare_data(
        self,
        df
    ):

        feature_engineer = FeatureEngineer()


        df = feature_engineer.create_features(
            df
        )


        df = df.dropna()



        X = df[
            FEATURE_COLUMNS
        ]


        y = df[
            "target"
        ]


        return X, y



    # -------------------------
    # TRAIN TEST SPLIT
    # -------------------------

    def split_data(
        self,
        X,
        y
    ):


        return train_test_split(

            X,

            y,

            test_size=0.20,

            shuffle=False

        )



    # -------------------------
    # METRICS
    # -------------------------

    def evaluate(
        self,
        y_true,
        predictions
    ):


        mae = mean_absolute_error(
            y_true,
            predictions
        )


        rmse = np.sqrt(
            mean_squared_error(
                y_true,
                predictions
            )
        )


        r2 = r2_score(
            y_true,
            predictions
        )


        return {


            "mae": float(mae),

            "rmse": float(rmse),

            "r2": float(r2)

        }



    # -------------------------
    # SAVE MODEL
    # -------------------------

    def save(
        self,
        model
    ):


        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )


        filename = (

            f"{self.symbol}_"
            f"{self.model_name}_"
            f"{timestamp}.pkl"

        )


        path = os.path.join(

            self.model_dir,

            filename

        )


        save_model(

            model,

            path

        )


        return path




    # -------------------------
    # MAIN TRAIN FUNCTION
    # -------------------------

    def train(self):


        # 1. Load data

        df = self.load_data()



        # 2. Prepare features

        X, y = self.prepare_data(
            df
        )



        # 3. Split

        X_train, X_test, y_train, y_test = self.split_data(
            X,
            y
        )



        # 4. Create model dynamically

        model = ModelFactory.create(
            self.model_name
        )



        # 5. Train

        model.train(

            X_train,

            y_train

        )



        # 6. Predict

        predictions = model.predict(
            X_test
        )



        # 7. Evaluate

        metrics = self.evaluate(

            y_test,

            predictions

        )



        # 8. Save

        model_path = self.save(
            model.model
        )



        # 9. Register

        self.registry.register_model(

            symbol=self.symbol,

            model_name=self.model_name,

            model_path=model_path,

            metrics=metrics,

            features=FEATURE_COLUMNS

        )



        return {


            "symbol": self.symbol,


            "model": self.model_name,


            "model_path": model_path,


            "metrics": metrics


        }
