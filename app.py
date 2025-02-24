from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run
from fastapi import FastAPI, File, UploadFile,Request
import pandas as pd
from sensor.utils.main_utils import load_object
from sensor.entity.estimator import apsModel

from sensor.aws_connection_s3 import S3_connection

from sensor.Exception import apsException
from sensor.logger import logging
from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.Constants import APP_HOST, APP_PORT

from typing import Optional


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()

        train_pipeline.run_pipeline()

        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")
    


@app.post("/predict")
async def predictRouteClient(request: Request,file: UploadFile =File(...)):
    df=pd.read_csv(file.file)
    print(df)
    preprocesor=load_object("final_model/preprocessing.pkl")
    #final_model=S3_connection.download_model_s3()
    final_model=load_object("final_model/model.pkl")
    network_model = apsModel(preprocessing_object=preprocesor,trained_model_object=final_model)
    #logging.info('model loaded from s3 in app.py for prediction')
    print(df.iloc[0])
    y_pred = network_model.predict(df)
    print(y_pred)
    df['predicted_column'] = y_pred
    print(df['predicted_column'])
    df.to_csv('prediction_output/output.csv')
    table_html = df.to_html(classes='table table-striped')

    print(table_html)
    return templates.TemplateResponse("index.html", {"request": request, "table": table_html})




if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)    