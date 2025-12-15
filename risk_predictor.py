from fastapi import FastAPI
import pickle
import pandas as pd
from fastapi.responses import JSONResponse
from pydantic import BaseModel

with open("model.pkl","rb") as file:
    model = pickle.load(file)

app = FastAPI()

class User(BaseModel):
    Age: int
    Gender:str
    BMI:float
    Smoking_Status: str
    Sleep_Duration: float
    Chronic_Disease_History: str
    Stress_Level:int

@app.get("/")
def read_root():
    return {"Hello": "You can test you health risk using our predictor(api)"}
@app.post("/predict")
def predict_risk(data: User):
    test_data=pd.DataFrame([{
        'Age':data.Age,
        'Gender':data.Gender,
        'BMI':data.BMI,
        'Smoking Status':data.Smoking_Status,
        'Sleep Duration':data.Sleep_Duration,
        'Chronic Disease History': data.Chronic_Disease_History,
        'Stress Level':data.Stress_Level
        }])
    prediction=model.predict(test_data)[0]
    return JSONResponse(status_code=200,content={"prediction category":prediction})