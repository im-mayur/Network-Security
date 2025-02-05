from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact
from networksecurity.constant.training_pipeline import MODEL_TRAINER_THRESHOULD,MODEL_TRAINER_EXPECTED_SCORE
from networksecurity.utils.main_utils.utils import save_pickle,load_object,load_np_array
from networksecurity.utils.ml_utils.model import estimator
from networksecurity.utils.ml_utils.metric import classification_metric

import os
import sys
import numpy as np
import pandas as pd


class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_config:ModelTrainerConfig):
        self.data_transformation_artifact=data_transformation_artifact
        self.model_trainer_config=model_trainer_config

    def train_model(self,X_data,y_data):
        pass

    def initiate_model_trainer(self):
        try:
            # load the train and test data from DataTransformationArtifact
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            train_arr=load_np_array(train_file_path)
            test_arr=load_np_array(test_file_path)

            X_train,y_train,X_test,y_test=[
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            ]
        except Exception as e:
            raise NetworkSecurityException(e,sys)