from datetime import datetime
import os

from networksecurity.constant import training_pipeline


class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
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
                                                training_pipeline.DATA_INJESTION_DIR_NAME,training_pipeline.TEST_FILE_NAME)

        self.train_test_split_ratio:float=training_pipeline.DATA_INJESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name:str=training_pipeline.DATA_INJESTION_COLLECTION_NAME
        self.database_name:str=training_pipeline.DATA_INJESTION_DATABASE_NAME


