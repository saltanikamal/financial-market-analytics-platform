import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)


def walk_forward_validation(
    model,
    X,
    y,
    folds=5
):
    """
    Walk-forward validation for time-series classification.

    Uses an expanding training window.

    Example with 5 folds:

        Fold 1:
            Train: first block
            Test:  next block

        Fold 2:
            Train: first two blocks
            Test:  next block

        ...

    No random shuffling is used.

    Returns:
        Dictionary containing validation metrics.
    """

    total_rows = len(X)

    test_size = total_rows // (folds + 1)

    predictions = []
    actuals = []
    probabilities = []

    completed_folds = 0

    for fold in range(1, folds + 1):

        print(f"\nFold {fold}")

        train_end = test_size * fold

        test_end = train_end + test_size

        if test_end > total_rows:
            break

        X_train = X.iloc[:train_end]
        y_train = y.iloc[:train_end]

        X_test = X.iloc[train_end:test_end]
        y_test = y.iloc[train_end:test_end]

        print(f"Train rows: {len(X_train)}")
        print(f"Test rows: {len(X_test)}")

        # ==========================
        # TRAIN
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
        # PROBABILITIES
        # ==========================

        if hasattr(model.model, "predict_proba"):

            fold_probabilities = model.model.predict_proba(
                X_test
            )

            probabilities.extend(
                fold_probabilities
            )

        completed_folds += 1

    # ==========================
    # CONVERT TO ARRAYS
    # ==========================

    predictions = np.array(
        predictions
    )

    actuals = np.array(
        actuals
    )

    # ==========================
    # CLASSIFICATION METRICS
    # ==========================

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

    # ==========================
    # ROC-AUC
    # ==========================

    roc_auc = 0.0

    if len(probabilities) > 0:

        try:

            probabilities = np.array(
                probabilities
            )

            roc_auc = roc_auc_score(
                actuals,
                probabilities,
                multi_class="ovr"
            )

        except Exception as e:

            print(
                f"ROC-AUC calculation failed: {e}"
            )

            roc_auc = 0.0

    # ==========================
    # RESULTS
    # ==========================

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
            completed_folds
    }

    print(
        "\nWalk-forward results"
    )

    print(
        results
    )

    return results
