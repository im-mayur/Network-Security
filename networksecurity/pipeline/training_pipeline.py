from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.constant.training_pipeline import TRAINING_BUCKET_NAME
from networksecurity.cloud.s3_syncer import s3sync 

from networksecurity.components.data_injestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import(
    TrainingPipelineConfig,
    DataInjestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig

)

from networksecurity.entity.artifact_entity import(
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

import os
import sys

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
        self.s3sync= s3sync()

    def data_ingestion(self):
        try:
            self.data_ingestion_config=DataInjestionConfig(training_pipeline_config=self.training_pipeline_config)

            logging.info("Started Data Ingestion")
            data_ingestion=DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info("Completed Data Ingestion")

            return data_ingestion_artifact

        except Exception as e:
            logging.error("Data ingestion failed")
            raise NetworkSecurityException(e,sys)
            
    
    def data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_validation_config=DataValidationConfig(self.training_pipeline_config)

            data_validation=DataValidation(data_injestion_artifact=data_ingestion_artifact,
                                           data_validation_config=data_validation_config)
            
            logging.info("Started Data validation")
            data_validation_artifact=data_validation.data_validation()
            logging.info("Completed Data Validation")

            return data_validation_artifact

        except Exception as e:
            logging.error("Data validation failed")
            raise NetworkSecurityException(e,sys)
        
    def data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config=DataTransformationConfig(self.training_pipeline_config)

            data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,
                                                   data_transformation_config=data_transformation_config)
            
            logging.info("Started Data Transformation")
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            logging.info("Completed Data Transformation")

            return data_transformation_artifact

        except Exception as e:
            logging.error("Data transformation failed")
            raise NetworkSecurityException(e,sys)
        
    def model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            model_trainer_config=ModelTrainerConfig(self.training_pipeline_config)
            
            model_trainer=ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                       model_trainer_config=model_trainer_config)
            
            logging.info("Started Model Training")
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            logging.info("Completed Model Training")

            return model_trainer_artifact

        except Exception as e:
            logging.error("Model Trainer failed")
            raise NetworkSecurityException(e,sys)
        
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url=f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3sync.sync_folder_to_s3(folder=self.training_pipeline_config.artifacts_dir,aws_bucket_url=aws_bucket_url)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def sync_model_dir_to_s3(self):
        try:
            aws_bucket_url=f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3sync.sync_folder_to_s3(folder=self.training_pipeline_config.model_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

        

    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.data_ingestion()
            data_validation_artifact=self.data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainet_artifact=self.model_trainer(data_transformation_artifact=data_transformation_artifact)

            self.sync_artifact_dir_to_s3()
            self.sync_model_dir_to_s3()

            return model_trainet_artifact

        except Exception as e:
            logging.error("Running pipelie failed")
            raise NetworkSecurityException(e,sys)

        



        

