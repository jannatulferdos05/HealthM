from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
from fastapi.responses import JSONResponse
from pydantic import BaseModel

with open("model.pkl","rb") as file:
    model = pickle.load(file)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    return {"Hello": "You can test your health risk using our predictor(api)"}
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
    return JSONResponse(status_code=200,content={"prediction_category":prediction})