from networksecurity.components.data_injestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataInjestionConfig,DataValidationConfig
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
        print(data_injestion_artifact)
        data_val_config=DataValidationConfig(train_config)

        logging.info("initiated data validation")
        data_validation=DataValidation(data_injestion_artifact,data_val_config)
        data_validation_artifact=data_validation.data_validation()
        print(data_validation_artifact)
        logging.info("data validation completed")
        

    except Exception as e:
        raise NetworkSecurityException(e,sys)