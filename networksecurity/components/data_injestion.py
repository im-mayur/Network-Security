from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataInjestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection  import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self,data_ingestion_config:DataInjestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self):
        '''
        This function reads the collection from mongoDb database as pandas dataframe
        '''
        try:
            database=self.data_ingestion_config.database_name
            collection=self.data_ingestion_config.collection_name

            # make the connection to mongoDB 
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL, serverSelectionTimeoutMS=10000)

            # get collection
            collection=self.mongo_client[database][collection]

            # read the collection as pandas dataframe 
            df=pd.DataFrame(list(collection.find()))

            # remove the default '_id' column
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)

            df.replace({"na":np.nan},inplace=True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_to_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path

            # returns a string value which represents the directory name from the specified path.
            feature_dir=os.path.dirname(feature_store_file_path)

            # make directory
            os.makedirs(feature_dir,exist_ok=True)

            # Save the CSV file to a Specified Location
            dataframe.to_csv(feature_store_file_path,index=False,header=True)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            
            train_set, test_set = train_test_split(
             dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            logging.info("Performed train test split on dataframe")
            
            logging.info("Started 'split_data_as_train_test' method of 'DataIngestion' class")



            train_file_path=self.data_ingestion_config.training_file_path
            test_file_path=self.data_ingestion_config.testing_file_path

            dir_path=os.path.dirname(train_file_path)

            # make the 'injested' folder 
            os.makedirs(dir_path,exist_ok=True)

            logging.info("Exporting the train and test set to 'ingested folder'")
            train_set.to_csv(train_file_path,index=False,header=True)
            test_set.to_csv(test_file_path,index=False,header=True)
            logging.info("Successfully exported train and test data to 'ingested folder' ")


        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            # call the 'export_collection_as_dataframe' to get pd dataframe
            dataframe=self.export_collection_as_dataframe()

            # export the dataframe as csv file to 'feature store'
            self.export_data_to_feature_store(dataframe)

            # export tarin and test data to 'injested folder'
            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact=DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path,
                                                          test_file_path=self.data_ingestion_config.testing_file_path)
            
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)



