from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import yaml
import os,sys
import dill
import numpy as np
import pickle


def read_yaml_file(filepath:str)->dict:
    try:
        with open(filepath, 'rb') as yamlfile:
            return yaml.load(yamlfile, Loader=yaml.SafeLoader)
    except Exception as e:
        NetworkSecurityException(e,sys)

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

def save_numpy_array(filepath:str, array:np.array):
    try:
        dir_name=os.path.dirname(filepath)
        os.makedirs(dir_name,exist_ok=True)
        with open(filepath,'wb') as file_obj:
            np.save(file_obj,array)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_pickle(filepath:str, obj:object):
    try:
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        
        #  If filepath does not exist, 'wb' will create a new file and write to it.
        with open(filepath,'wb') as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


