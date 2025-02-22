from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.constant.training_pipeline import MODEL_TRAINER_THRESHOULD,MODEL_TRAINER_EXPECTED_SCORE
from networksecurity.utils.main_utils.utils import save_pickle,load_object,load_np_array,evaluate_model
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier

import os
import sys
from typing import Literal
import numpy as np
import pandas as pd
import mlflow
import dagshub
# dagshub.init(repo_owner='im-mayur', repo_name='Network-Security', mlflow=True)

class ModelTrainer:
    '''
    This class retrives the train and test file path from "DataTransformationArtifact" 
    and creates the "model.pkl" with best model and best parameter.
    '''

    def __init__(self,data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_config:ModelTrainerConfig):
        self.data_transformation_artifact=data_transformation_artifact
        self.model_trainer_config=model_trainer_config

    def track_mlflow(self,best_model,classification_metric,type:Literal["train", "test"] ):
        with mlflow.start_run():
            if type=="train":
                f1_score=classification_metric.f1_score
                precision_score=classification_metric.precision_score
                recall_score=classification_metric.recall_score

                mlflow.log_metric("train_f1_score",f1_score)
                mlflow.log_metric("train_precision_score",precision_score)
                mlflow.log_metric("train_recall_score",recall_score)
                mlflow.sklearn.log_model(best_model,"best_model")

            elif type=="test":
                f1_score=classification_metric.f1_score
                precision_score=classification_metric.precision_score
                recall_score=classification_metric.recall_score

                mlflow.log_metric("test_f1_score",f1_score)
                mlflow.log_metric("test_precision_score",precision_score)
                mlflow.log_metric("test_recall_score",recall_score)
                mlflow.sklearn.log_model(best_model,"best_model")
            

            


            

    def train_model(self,X_train,y_train, X_test,y_test)->ModelTrainerArtifact:
        '''
        This function conatins models and hyperparametes to be passsed to the GridSearchCV.
        Finds the best model and best parameters to be saved as pickle file.
        '''

        # Algorithms to try
        models={
            "Decision Tree":DecisionTreeClassifier(),
            "Random Forest":RandomForestClassifier(),
            "Gradient Boosting":GradientBoostingClassifier(),
            "Logistic Regression":LogisticRegression(),
            "AdaBoost Classifier":AdaBoostClassifier(),
            "KneighborClassifier":KNeighborsClassifier(),          
        }

        # parameters for hyperparameter tuning
        params={
                "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                'splitter':['best','random'],
                'max_features':['sqrt','log2'],
            },    
            "Random Forest":{
                'criterion':['gini', 'entropy', 'log_loss'],
                
                'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                # 'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                'max_features':['auto','sqrt','log2'],
                # 'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{
                "penalty":['l1', 'l2', 'elasticnet', None]
            },
            "AdaBoost Classifier":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64]
            },
            "KneighborClassifier":{
                "n_neighbors":[3,5,7],
                "algorithm":['auto', 'ball_tree', 'kd_tree', 'brute']
            }
        }

        # Dictionary with format as--
        # {model:{test_model_score:float},
        #        best_params:{grid.best_params_}
        #          }
        
        model_report:dict=evaluate_model(X_train=X_train,y_train=y_train,
                                         X_test=X_test,y_test=y_test,
                                         models=models,params=params)
        
        print(model_report)
        logging.info(f"model report:\n {model_report}")

        #get the best r2_score form model_report dictionary
        best_model_score= max([info["test_model_score"] for info in model_report.values()])

        # based on the 'best_model_score' get the corresponding 'best_model' and 'best_params'
        for model,info in model_report.items():
            if info["test_model_score"]==best_model_score:
                best_model_name=model
                best_params=info["best_params"]

        best_model=models[best_model_name]

        # pass the best_params as key:val pairs
        best_model.set_params(**best_params)
        print(f"best model:\n {best_model_name}")
        print(f"best parameter: {best_params}")
        logging.info(f"best model: {best_model_name}")
        logging.info(f"best parameter: {best_params}")
        
        # fit the best_model to train on X_train,y_train
        best_model.fit(X_train, y_train) 
        y_train_pred=best_model.predict(X_train)

        # calculate the f1_score, precison_score, recall_score for y_train
        classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)
        logging.info(f"classification train matric: \n {classification_train_metric}")

        ### Track mlflow for train metrics
        self.track_mlflow(best_model,classification_train_metric,type='train')

         # calculate the f1_score, precison_score, recall_score for y_test
        y_test_pred=best_model.predict(X_test)
        classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)
        logging.info(f"classification test matric: \n {classification_test_metric}")

        ### Track mlflow for test metrics
        self.track_mlflow(best_model,classification_test_metric,type='test')

        # read the 'preprocessing.pkl' which is KNNImputer object
        preprocessor=load_object(self.data_transformation_artifact.transformed_obj_file_path)

        # create 'trained_model' folder inside 'model_trainer'
        model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_path)
        os.makedirs(model_dir_path,exist_ok=True)

        # create the object of NetworkModel method form estimator.py
        # and save it as 'model.pkl'
        Network_Model= NetworkModel(preprocessor,best_model)
        save_pickle(filepath=self.model_trainer_config.trained_model_path,obj=Network_Model)

        save_pickle("final_model/model.pkl",best_model)

        #model trainer artifact
        return ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric,
            )

    def initiate_model_trainer(self):
        try:
            # load the train and test data from DataTransformationArtifact
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            # read the .npy files 
            train_arr=load_np_array(train_file_path)
            test_arr=load_np_array(test_file_path)

            X_train,y_train,X_test,y_test=[
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            ]

            model_trainer_artifact=self.train_model(X_train=X_train,y_train=y_train,
                                                     X_test=X_test,y_test=y_test)
            
            logging.info(model_trainer_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)