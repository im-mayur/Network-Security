import datetime
import os
import logging
import json

import pandas as pd
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

data=pd.read_csv('Network_Data/phisingData.csv')

data.reset_index(drop=True, inplace=True)

new_data=data.head(2)

print(list(json.loads(data.T.to_json()).values()))
# records=data.to_json()
# print(records)
