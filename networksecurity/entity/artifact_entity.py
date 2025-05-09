from dataclasses import dataclass



'''
The dataclass provides an in built __init__() constructor to classes which handle the 
data and object creation for them. 
'''

@dataclass
class DataIngestionArtifact:
    train_file_path:str
    test_file_path:str


@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str

@dataclass
class DataTransformationArtifact:
    transformed_obj_file_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str


@dataclass
class ClassifiactionMetricArtifact:
    f1_score:float
    precision_score:float
    recall_score:float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str
    train_metric_artifact:ClassifiactionMetricArtifact
    test_metric_artifact:ClassifiactionMetricArtifact