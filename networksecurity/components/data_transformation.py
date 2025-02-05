from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.utils.main_utils.utils import save_numpy_array,save_pickle

import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

class DataTransforrmation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(filepath)->pd.DataFrame:
        print("reading the data for transformation")
        return pd.read_csv(filepath)
    

    def get_data_transformation_obj(cls):
        try:
            logging.info("Enterted the get_data_transformation_obj method of DataTransformation class")
            print("Enterted the get_data_transformation_obj method of DataTransformation class")

            # ** indiactes that passed param is key value pair
            logging.info("Initiated KNNImpuatation")
            print("Initiated KNNImpuatation")
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor:Pipeline=Pipeline([("imputer",imputer)])

            return processor
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)

        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Initiated data transformation")

            # read the tarain and test data as pandas dataframne
            train_df=DataTransforrmation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransforrmation.read_data(self.data_validation_artifact.valid_test_file_path)

            # remove target column
            train_feature_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_train_df=train_df[TARGET_COLUMN]
            target_train_df=target_train_df.replace(-1, 0)

            test_feature_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_test_df=test_df[TARGET_COLUMN]
            target_test_df=target_test_df.replace(-1,0)

            # transform the train and test data with pipeline object
            preprocessor=self.get_data_transformation_obj()


            preprocessor_obj = preprocessor.fit(train_feature_df)
            transformed_train_df = preprocessor_obj.transform(train_feature_df)
            transformed_test_df = preprocessor_obj.transform(test_feature_df)

            logging.info("Completed the data transformaation with preprocesssing pipeline")
            print("Completed the data transformaation with preprocesssing pipeline")

            # arrays will be stacked along their last axis
            train_arr=np.c_[transformed_train_df,np.array(target_train_df)]
            test_arr=np.c_[transformed_test_df,np.array(target_test_df)]

            # save the transformed data as .npy file
            save_numpy_array(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path, test_arr)
            logging.info("saved the transformed data as .npy file")
            print("saved the transformed data as .npy file")

            # save preprocessor object as .pkl file
            save_pickle(self.data_transformation_config.preproceesor_file_path,preprocessor_obj)
            print("saved the preprocessor object as .pkl file")
            logging.info("saved the preprocessor object as .pkl file")

            # prepare DataTransformationArtifact
            print("prepared DataTransformationArtifact")
            logging.info("prepared DataTransformationArtifact")
            data_transformation_artifact=DataTransformationArtifact(
                transformed_obj_file_path=self.data_transformation_config.preproceesor_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
