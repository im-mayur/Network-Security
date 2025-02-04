from networksecurity.components.data_injestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataInjestionConfig
from networksecurity.constant import training_pipeline  
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys


if __name__=='__main__':
    try:
        train_config=TrainingPipelineConfig()
        data_config=DataInjestionConfig(train_config)
        data_injestion=DataIngestion(data_config)
        logging.info("Initiate data injestion")
        data_artifact=data_injestion.initiate_data_ingestion()
        

    except Exception as e:
        raise NetworkSecurityException(e,sys)