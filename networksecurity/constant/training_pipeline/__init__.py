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




'''
Data Injestion realated constants starts with DATA_INJESTION_VAR
'''

DATA_INJESTION_COLLECTION_NAME: str= "phisingData"
DATA_INJESTION_DATABASE_NAME: str= "NetworkData"
DATA_INJESTION_DIR_NAME: str= "data_injestion"
DATA_INJESTION_FEATURE_STORE_DIR: str= "feature_store"
DATA_INJESTION_INJESTED_DIR: str= "injested"
DATA_INJESTION_TRAIN_TEST_SPLIT_RATION: float= 0.2