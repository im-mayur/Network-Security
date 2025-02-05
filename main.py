from networksecurity.components.data_injestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransforrmation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataInjestionConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.constant import training_pipeline  
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys


if __name__=='__main__':
    try:
        train_config=TrainingPipelineConfig()
        data_config=DataInjestionConfig(train_config)
        data_injestion=DataIngestion(data_config)
        logging.info("Initiate data injestion")

        data_injestion_artifact=data_injestion.initiate_data_ingestion()
        print(data_injestion_artifact,"\n")
        data_val_config=DataValidationConfig(train_config)

        logging.info("initiated data validation")
        data_validation=DataValidation(data_injestion_artifact,data_val_config)
        data_validation_artifact=data_validation.data_validation()
        print(data_validation_artifact,'\n')
        logging.info("data validation completed")

        logging.info("initiated data transformation")
        data_transformation_config=DataTransformationConfig(train_config)
        data_transformation=DataTransforrmation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact,"\n")
        logging.info("completed data transformation")
        

    except Exception as e:
        raise NetworkSecurityException(e,sys)