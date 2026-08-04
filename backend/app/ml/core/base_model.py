from abc import ABC, abstractmethod


class BaseModel(ABC):
    """
    Abstract base class for all ML models.

    Every model must implement:

    - train()
    - predict()
    - predict_proba()
    - evaluate()
    - get_feature_importance()
    - save()
    - load()

    Classification labels:

        0 = SELL
        1 = HOLD
        2 = BUY
    """


    def __init__(self):

        self.model = None



    @abstractmethod
    def train(self, X_train, y_train):
        """
        Train the model.
        """
        pass



    @abstractmethod
    def predict(self, X):
        """
        Generate class predictions.
        """
        pass



    @abstractmethod
    def predict_proba(self, X):
        """
        Generate class probabilities.

        Example:

        [
            [0.80, 0.15, 0.05],
            [0.10, 0.20, 0.70]
        ]

        Columns correspond to:

        0 = SELL
        1 = HOLD
        2 = BUY
        """
        pass



    @abstractmethod
    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance.
        """
        pass



    @abstractmethod
    def get_feature_importance(self):
        """
        Return feature importance values.

        Used for:
        - model explainability
        - dashboard visualization
        - analysis
        """
        pass



    @abstractmethod
    def save(self, filepath):
        """
        Save trained model.
        """
        pass



    @abstractmethod
    def load(self, filepath):
        """
        Load trained model.
        """
        pass
