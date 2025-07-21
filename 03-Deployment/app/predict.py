from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import pickle
from prepare_data import preprocess_data

app = FastAPI()

# Load model and preprocessor
with open("/app/model/model.pkl", "rb") as f:
    model = pickle.load(f)

preprocessor = joblib.load("/app/model/preprocessor.joblib")

class CrashInput(BaseModel):
    posted_speed_limit: int
    weather_condition: str
    lighting_condition: str
    first_crash_type: str
    trafficway_type: str
    roadway_surface_cond: str
    prim_contributory_cause: str
    crash_hour: int
    delay_police_minutes: float

@app.post("/predict")
def predict(input_data: CrashInput):
    df = pd.DataFrame([input_data.dict()])
    X = preprocessor.transform(df)
    pred = model.predict(X)
    return {"prediction": int(pred[0])}
