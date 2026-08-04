import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)



def walk_forward_validation(
    model,
    X,
    y,
    folds=5
):
    """
    Walk-forward validation for time-series classification.

    Uses expanding window:

    Fold 1:
        Train: first 344 rows
        Test: next 172 rows

    Fold 2:
        Train: first 516 rows
        Test: next 172 rows

    ...

    Parameters:
        model:
            ML wrapper model
            (XGBoostModel / RandomForestModel)

        X:
            Feature dataframe

        y:
            Target series

        folds:
            Number of validation folds


    Returns:
        Dictionary of validation metrics
    """


    total_rows = len(X)


    test_size = total_rows // (folds + 1)



    predictions = []

    actuals = []



    for fold in range(1, folds + 1):


        print(
            f"\nFold {fold}"
        )


        train_end = (
            test_size * fold
        )


        test_end = (
            train_end + test_size
        )


        if test_end > total_rows:

            break



        X_train = X.iloc[
            :train_end
        ]


        y_train = y.iloc[
            :train_end
        ]



        X_test = X.iloc[
            train_end:test_end
        ]


        y_test = y.iloc[
            train_end:test_end
        ]



        print(
            f"Train rows: {len(X_train)}"
        )


        print(
            f"Test rows: {len(X_test)}"
        )



        # ==========================
        # TRAIN WRAPPER MODEL
        # ==========================

        model.train(
            X_train,
            y_train
        )



        # ==========================
        # PREDICT
        # ==========================

        y_pred = model.predict(
            X_test
        )



        predictions.extend(
            y_pred
        )


        actuals.extend(
            y_test
        )



    # ==========================
    # FINAL VALIDATION METRICS
    # ==========================


    predictions = np.array(
        predictions
    )


    actuals = np.array(
        actuals
    )



    accuracy = accuracy_score(
        actuals,
        predictions
    )


    precision = precision_score(
        actuals,
        predictions,
        average="weighted",
        zero_division=0
    )


    recall = recall_score(
        actuals,
        predictions,
        average="weighted",
        zero_division=0
    )


    f1 = f1_score(
        actuals,
        predictions,
        average="weighted",
        zero_division=0
    )



    # ROC AUC for multiclass
    try:

        if hasattr(model.model, "predict_proba"):

            probabilities = (
                model.model.predict_proba(X.iloc[-len(actuals):])
            )


            roc_auc = roc_auc_score(
                actuals,
                probabilities,
                multi_class="ovr"
            )

        else:

            roc_auc = 0.0


    except Exception:

        roc_auc = 0.0



    results = {

        "accuracy": round(
            float(accuracy),
            4
        ),

        "precision": round(
            float(precision),
            4
        ),

        "recall": round(
            float(recall),
            4
        ),

        "f1": round(
            float(f1),
            4
        ),

        "roc_auc": round(
            float(roc_auc),
            4
        ),

        "validation_method":
            "walk_forward",

        "folds":
            folds - 1

    }


    print(
        "\nWalk-forward results"
    )


    print(
        results
    )


    return results
