from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

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
    

def load_object(filepath:str):
    try:
        with open(filepath, 'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def load_np_array(filepath:str):
    try:
        with open(filepath, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

def evaluate_model(X_train,y_train,X_test,y_test,models,params)->dict:
    try:
        report={}
        
        for i in list(models.keys()):
            model=models[i]
            param=params[i]

            grid=GridSearchCV(estimator=model,
                              param_grid=param,cv=3)
            print("Tunning the model",str(model))
            logging.info(f"Tuning the model: {model}")
            grid.fit(X_train,y_train)

            model.fit(X_train,y_train)
            model.set_params(**grid.best_params_)
           

            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)

            test_model_score=r2_score(y_true=y_test,y_pred=y_test_pred)

            report[i]={"test_model_score":test_model_score,
                                            "best_params":grid.best_params_}
            

        return report
        

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    



