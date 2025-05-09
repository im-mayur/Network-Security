'''
This is ETL pipeline.

--> Data is extracted from 'phisingData.csv' in 'Network_Data' folder.
--> Then Data in csv format is converted to json format.
--> This data is then pushed to mondoDB database.

Note: If you encounter [Server connection timed out error] while pushing the data to mongoDB database,
      consider checking if 'current ip' is added to cluster. 
      (Go to mongo atlas homepage--> select cluster--> Network access--> Add current ip)
'''


import os
import json
import sys
from dotenv import load_dotenv
load_dotenv()

import certifi
ca=certifi.where()

import pymongo

import pandas as pd 
import numpy as np 

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

# get the mongodb_url from .env file
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
# print(MONGO_DB_URL)

class NetworkDataExtractor():
    '''
    This class implements ETL pipeline to extract, transform and load the data.
    '''
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_converter(self,filepath):
        '''
        This function converts csv data to json format.

        parameters:
        filepath:path of the csv dataset file.(str)
        '''
        try:
            data=pd.read_csv(filepath)
            data.reset_index(drop=True, inplace=True)

            # 1) Convert DataFrame to JSON
            # 2) json.loads() converts the JSON string back into a Python dictionary.
            # 3) .values() retrives the the values from dictionary
            records=list(json.loads(data.T.to_json()).values())

            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_to_mongodb(self,records,collection,database):
        '''
        Push the json data to mongoDB database.

        Parameter:
        records:json data(nested list)
        collection:Name of the collection (table) to be created(str)
        database: Name of the database to br created(str)
        '''
        try:
            self.records=records
            self.collection=collection
            self.database=database

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)

            # create database
            self.database=self.mongo_client[self.database]

            # create collection(table) in database
            self.collection=self.database[self.collection]

            # add records(data) in doctionary format
            self.collection.insert_many(self.records)
            return len(self.records)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

if __name__=='__main__':
    filepath='Network_Data/phisingData.csv'
    DATABASE="NetworkData"
    COLLECTION='phisingData'
    etl_obj=NetworkDataExtractor()
    records=etl_obj.csv_to_json_converter(filepath=filepath)
    success=etl_obj.insert_data_to_mongodb(database=DATABASE,collection=COLLECTION,records=records)
    print("data is successfully added to mongoDB, total records added", success)





