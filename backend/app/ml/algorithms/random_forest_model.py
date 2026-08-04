import joblib
from pathlib import Path

import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from app.ml.core.base_model import BaseModel


class RandomForestModel(BaseModel):
    """
    Random Forest classification model.

    Classes:

        0 = SELL
        1 = HOLD
        2 = BUY
    """


    def __init__(self):

        super().__init__()


        self.model = RandomForestClassifier(

            n_estimators=300,

            max_depth=8,

            min_samples_split=10,

            min_samples_leaf=5,

            class_weight="balanced",

            random_state=42,

            n_jobs=-1
        )



    # =====================================
    # TRAIN
    # =====================================

    def train(self, X_train, y_train):

        self.model.fit(
            X_train,
            y_train
        )

        return self.model



    # =====================================
    # PREDICT
    # =====================================

    def predict(self, X):

        return self.model.predict(X)



    # =====================================
    # PREDICT PROBABILITY
    # =====================================

    def predict_proba(self, X):

        return self.model.predict_proba(X)



    # =====================================
    # EVALUATE
    # =====================================

    def evaluate(self, X_test, y_test):

        predictions = self.predict(
            X_test
        )


        probabilities = self.predict_proba(
            X_test
        )


        results = {

            "accuracy": float(
                accuracy_score(
                    y_test,
                    predictions
                )
            ),


            "precision": float(
                precision_score(
                    y_test,
                    predictions,
                    average="weighted",
                    zero_division=0
                )
            ),


            "recall": float(
                recall_score(
                    y_test,
                    predictions,
                    average="weighted",
                    zero_division=0
                )
            ),


            "f1": float(
                f1_score(
                    y_test,
                    predictions,
                    average="weighted",
                    zero_division=0
                )
            )

        }


        try:

            results["roc_auc"] = float(
                roc_auc_score(
                    y_test,
                    probabilities,
                    multi_class="ovr"
                )
            )


        except Exception:

            results["roc_auc"] = 0.0



        return results



    # =====================================
    # FEATURE IMPORTANCE
    # =====================================

    def get_feature_importance(self, feature_names=None):

        importance = self.model.feature_importances_


        if feature_names is None:

            return {

                str(i): float(value)

                for i, value
                in enumerate(importance)

            }


        return {

            name: float(value)

            for name, value
            in zip(
                feature_names,
                importance
            )

        }



    # =====================================
    # SAVE
    # =====================================

    def save(self, filepath):

        Path(filepath).parent.mkdir(

            parents=True,

            exist_ok=True

        )


        joblib.dump(

            self.model,

            filepath

        )



    # =====================================
    # LOAD
    # =====================================

    def load(self, filepath):

        self.model = joblib.load(

            filepath

        )

        return self.model
