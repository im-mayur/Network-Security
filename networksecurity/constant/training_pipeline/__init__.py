import os
import sys
import numpy as np
import pandas as pd

'''
Defining common constatnt variable for training pipeline
'''

TRAGET_COLUMN="Result"
PIPELINE_NAME: str="NetworkSecurity"
ARTIFACTS_DIR: str="Artifacts"
FILE_NAME: str="PhisingData.csv"

TRAIN_FILE_NAME: str="train.csv"
TEST_FILE_NAME: str="test.csv"

SCHEMA_FILE_PATH: str=os.path.join("data_schema","schema.yaml")




'''
Data Injestion realated constants starts with DATA_INJESTION_VAR
'''

DATA_INJESTION_COLLECTION_NAME: str= "phisingData"
DATA_INJESTION_DATABASE_NAME: str= "NetworkData"
DATA_INJESTION_DIR_NAME: str= "data_injestion"
DATA_INJESTION_FEATURE_STORE_DIR: str= "feature_store"
DATA_INJESTION_INJESTED_DIR: str= "injested"
DATA_INJESTION_TRAIN_TEST_SPLIT_RATION: float= 0.2


'''
Data Validation related constants starts with DATA_VALIDATION_VAR
'''

DATA_VALIDATION_DIR_NAME: str="data_validation"
DATA_VALIDATION_VALID_DIR: str="validated"
DATA_VALIDATION_INVALID_DIR: str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILENAME: str="report.yaml"