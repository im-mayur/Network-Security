from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.artifact_entity import ClassifiactionMetricArtifact
import sys
import os
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME


class NetworkModel:
    def __init__(self,preprocessor,model):
        self.preprocessor=preprocessor
        self.model=model

    def predict(self,x):
        X_transform=self.preprocessor.transform(x)
        y_hat=self.model.predict(X_transform)

        return y_hat