from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.artifact_entity import ClassifiactionMetricArtifact
from sklearn.metrics import f1_score,precision_score,recall_score
import sys


def get_classification_score(y_true,y_pred)->ClassifiactionMetricArtifact:
    try:
        model_f1_score=f1_score(y_true,y_pred)
        model_precision_score=precision_score(y_true,y_pred)
        model_recall_score=recall_score(y_true,y_pred)

        model_score=ClassifiactionMetricArtifact(
            model_f1_score,
            model_precision_score,
            model_recall_score
        )

        return model_score
    except Exception as e:
        raise NetworkSecurityException(e,sys)