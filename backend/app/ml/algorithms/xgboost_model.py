import joblib

from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from sklearn.utils.class_weight import compute_sample_weight

from xgboost import XGBClassifier

from app.ml.core.base_model import BaseModel



class XGBoostModel(BaseModel):
    """
    XGBoost multiclass classification model.

    Classes:

        0 = SELL
        1 = HOLD
        2 = BUY

    """



    def __init__(self):

        super().__init__()


        self.model = XGBClassifier(

            n_estimators=400,

            learning_rate=0.03,

            max_depth=5,

            subsample=0.8,

            colsample_bytree=0.8,

            objective="multi:softprob",

            num_class=3,

            eval_metric="mlogloss",

            random_state=42,

            n_jobs=-1

        )



    # =====================================================
    # TRAIN
    # =====================================================

    def train(
        self,
        X_train,
        y_train
    ):

        """
        Train XGBoost with balanced class weights.
        """


        sample_weights = compute_sample_weight(

            class_weight="balanced",

            y=y_train

        )


        self.model.fit(

            X_train,

            y_train,

            sample_weight=sample_weights

        )



    # =====================================================
    # PREDICT CLASS
    # =====================================================

    def predict(
        self,
        X
    ):

        return self.model.predict(

            X

        )



    # =====================================================
    # PREDICT PROBABILITY
    # =====================================================

    def predict_proba(
        self,
        X
    ):

        return self.model.predict_proba(

            X

        )



    # =====================================================
    # CLASSES PROPERTY
    # =====================================================

    @property
    def classes_(self):

        """
        Expose underlying XGBoost classes.

        Required by predictor.py

        Example:

        probabilities:

        [0.20, 0.50, 0.30]

        maps to:

        SELL = 20%
        HOLD = 50%
        BUY  = 30%

        """

        return self.model.classes_



    # =====================================================
    # EVALUATE
    # =====================================================

    def evaluate(
        self,
        X_test,
        y_test
    ):

        predictions = self.predict(

            X_test

        )


        probabilities = self.predict_proba(

            X_test

        )



        accuracy = accuracy_score(

            y_test,

            predictions

        )


        precision = precision_score(

            y_test,

            predictions,

            average="weighted",

            zero_division=0

        )


        recall = recall_score(

            y_test,

            predictions,

            average="weighted",

            zero_division=0

        )


        f1 = f1_score(

            y_test,

            predictions,

            average="weighted",

            zero_division=0

        )



        try:

            roc_auc = roc_auc_score(

                y_test,

                probabilities,

                multi_class="ovr"

            )


        except Exception:

            roc_auc = 0.0



        print("\nConfusion Matrix")

        print(

            confusion_matrix(

                y_test,

                predictions

            )

        )



        print("\nClassification Report")

        print(

            classification_report(

                y_test,

                predictions,

                zero_division=0

            )

        )



        return {

            "accuracy": float(accuracy),

            "precision": float(precision),

            "recall": float(recall),

            "f1": float(f1),

            "roc_auc": float(roc_auc)

        }



    # =====================================================
    # FEATURE IMPORTANCE
    # =====================================================

    def get_feature_importance(
        self,
        feature_names
    ):

        """
        Return feature importance as JSON serializable dict.
        """


        if not hasattr(

            self.model,

            "feature_importances_"

        ):

            return {}



        importance = self.model.feature_importances_



        feature_importance = {}



        for name, value in zip(

            feature_names,

            importance

        ):

            feature_importance[name] = float(value)



        return dict(

            sorted(

                feature_importance.items(),

                key=lambda x: x[1],

                reverse=True

            )

        )



    # =====================================================
    # SAVE
    # =====================================================

    def save(
        self,
        filepath
    ):


        Path(filepath).parent.mkdir(

            parents=True,

            exist_ok=True

        )


        joblib.dump(

            self.model,

            filepath

        )



    # =====================================================
    # LOAD
    # =====================================================

    def load(
        self,
        filepath
    ):


        self.model = joblib.load(

            filepath

        )
