from datetime import datetime
import os

from networksecurity.constant import training_pipeline


class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y")
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifacts_name=training_pipeline.ARTIFACTS_DIR

        # create thee folder named 'Artifacts'
        self.artifacts_dir=os.path.join(self.artifacts_name,timestamp)
        self.timestamp:str=timestamp


class DataInjestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):

        # create 'data_injestion' folder inside 'Artifacts'
        self.data_injestion_dir:str=os.path.join(
            training_pipeline_config.artifacts_dir,training_pipeline.DATA_INJESTION_DIR_NAME
        )

        # create 'feature_store' folder inside 'data_injestion'
        # insert 'phisingData' inside 'data_injestion' folder
        self.feature_store_file_path:str=os.path.join(self.data_injestion_dir, 
                                                      training_pipeline.DATA_INJESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME)
        
        # create 'injested' folder inside 'data_injestion'
        # create 'train.csv' inside 'injested'
        self.training_file_path:str=os.path.join(self.data_injestion_dir, 
                                                      training_pipeline.DATA_INJESTION_INJESTED_DIR,training_pipeline.TRAIN_FILE_NAME)
        
        # create 'injested' folder inside 'data_injestion'
        # create 'test.csv' inside 'injested'
        self.testing_file_path:str=os.path.join(self.data_injestion_dir,
                                                training_pipeline.DATA_INJESTION_INJESTED_DIR,training_pipeline.TEST_FILE_NAME)

        self.train_test_split_ratio:float=training_pipeline.DATA_INJESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name:str=training_pipeline.DATA_INJESTION_COLLECTION_NAME
        self.database_name:str=training_pipeline.DATA_INJESTION_DATABASE_NAME


class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        
        # data_validation folder inside 'Artifacts'
        self.data_validation_dir:str=os.path.join(
            training_pipeline_config.artifacts_dir,training_pipeline.DATA_VALIDATION_DIR_NAME
        )

        # 'validated' folder inside 'data_validation'
        self.valid_data_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)

        self.valid_train_file_path:str=os.path.join(self.valid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path:str=os.path.join(self.valid_data_dir,training_pipeline.TEST_FILE_NAME)
        
        # 'invalid' folder inside 'data_validation'
        self.invalid_data_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)

        self.invalid_train_file_path:str=os.path.join(self.invalid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path:str=os.path.join(self.invalid_data_dir,training_pipeline.TEST_FILE_NAME)

        # 'drift_report' folder inside 'data_validation'
        # 'report.yaml' inside 'drift_report'
        self.drift_report_file_path:str=os.path.join(self.data_validation_dir,
                                                     training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
                                                     training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILENAME)
        


class  DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        # create 'data_transformation' folder in 'Artifacts'
        self.data_transformation_dir: str=os.path.join(training_pipeline_config.artifacts_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME)

        # create 'tranformed' folder inside 'data_transformation'
        # create 'train.npy' inside 'transformed'
        self.transformed_train_file_path: str=os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,
                                                      training_pipeline.TRAIN_FILE_NAME.replace('csv','npy'))
        
        # create 'tranformed' folder inside 'data_transformation'
        # create 'train.npy' inside 'transformed'
        self.transformed_test_file_path: str=os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,
                                                      training_pipeline.TEST_FILE_NAME.replace('csv','npy'))
        
        # create 'transformed_object' folder inside 'data_transformation'
        # create 'preprocessing.pkl' inside 'transformed_object'
        self.preproceesor_file_path: str=os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_PREPROCESSOR_DIR,
                                                      training_pipeline.PREPROCESSOR_OBJ_FILE_NAME)
        



class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        # create 'Model_Trainer' folder inside 'Artifact'
        self.model_trainer_dir=os.path.join(training_pipeline_config.artifacts_dir,training_pipeline.MODEL_TRAINER_DIR)

        # create 'trained_model' folder inside 'Model_Trainer'
        self.trained_model_dir=os.path.join(self.model_trainer_dir,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR)

        # create 'model.pkl' inside 'trained_model'
        self.trained_model_path=os.path.join(self.trained_model_dir,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME)

        self.expected_accuracy=training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.fitting_threshould=training_pipeline.MODEL_TRAINER_THRESHOULD