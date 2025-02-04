from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
import os
import sys
import numpy as np
import pandas as pd

from scipy.stats import ks_2samp


class DataValidation:
    def __init__(self,data_injestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_injestion_artifact=data_injestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(filepath)->pd.DataFrame:
        return pd.read_csv(filepath)


    def validate_no_of_column(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_col=len(self._schema_config['columns'])
            logging.info(f"Required number of columns {number_of_col}")
            logging.info(f"Dataframe has total {len(dataframe.columns)}")

            if number_of_col==len(dataframe.columns):
                return True
            else:
                False

        except Exception as e:
            raise NetworkSecurityException(e,sys) 
        

    def check_num_columns(self,dataframe):
       numeric_cols = dataframe.select_dtypes(include=['number'])
       if len(numeric_cols.columns)>0:
           return True
       else:
           False

    def detect_drift(self,base_df,compare_df):
        try:
            status=True
            report={}
            for column in base_df:
                d1=base_df[column]
                d2=compare_df[column]
                ks_result=ks_2samp(d1,d2)
                if ks_result.pvalue>=0.05:
                    drift_found=False
                else:
                    drift_found=True
                    status=False

                report.update({column:{
                    "p_value":float(ks_result.pvalue),
                    "status":drift_found
                }})

            drift_report_file_path=self.data_validation_config.drift_report_file_path
        
            dir_path=os.path.dirname(drift_report_file_path)
            print(self.data_validation_config.drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(drift_report_file_path,content=report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def data_validation(self)->DataValidationArtifact:
        print("started data validation")
        try:
            train_file_path=self.data_injestion_artifact.train_file_path
            test_file_path=self.data_injestion_artifact.test_file_path

            # read the data from train and test 
            print("reading the data from train test")
            train_dataframe= DataValidation.read_data(train_file_path)
            test_dataframe= DataValidation.read_data(test_file_path)

            # validate number of columns
            print("validating number of columns")
            status=self.validate_no_of_column(dataframe=train_dataframe)
            if not status:
                error_message=f"Train dataset does not contain all the columns"

            status=self.validate_no_of_column(dataframe=test_dataframe)
            if not status:
                error_message=f"Test dataset does not contain all the columns"

            # detect data drift
            print("detecting data drift")
            status=self.detect_drift(base_df=train_dataframe,compare_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)


            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,
                                   index=False,header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,
                                   index=False,header=True)
            print("completed data valiadtion")
            return DataValidationArtifact(
                    validation_status=status,
                    valid_train_file_path=self.data_validation_config.valid_train_file_path,
                    valid_test_file_path=self.data_validation_config.valid_test_file_path,
                    invalid_train_file_path=None,
                    invalid_test_file_path=None,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path
                     )

            


        except Exception as e:
            raise NetworkSecurityException(e,sys) 


