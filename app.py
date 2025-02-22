import os
import sys

import certifi
ca=certifi.where()

import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")


from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd 


from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="./templates")

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.constant.training_pipeline import DATA_INJESTION_DATABASE_NAME,DATA_INJESTION_COLLECTION_NAME

client=pymongo.MongoClient(MONGO_DB_URL,tlsCAFile=ca)

database=client[DATA_INJESTION_DATABASE_NAME]
collection=database[DATA_INJESTION_COLLECTION_NAME]

app = FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successsful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.post("/predict")
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        preprocessor=load_object("final_model/preprocessor.pkl")
        model=load_object("final_model/model.pkl")
        networkmodel=NetworkModel(preprocessor=preprocessor,model=model)
        print(df.iloc[0])
        y_pred=networkmodel.predict(df)
        print(y_pred)

        df["Predicted_column"]=y_pred
        # df["Predicted_column"].replace(-1,0)

        df.to_csv("templates/valid_data/predicted.csv")
        table_html=df.to_html(classes='table table-striped')
        print(table_html)

        return templates.TemplateResponse("table.html", {"request":request, "table":table_html})


    except Exception as e:
        raise NetworkSecurityException(e,sys)



if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8080)
