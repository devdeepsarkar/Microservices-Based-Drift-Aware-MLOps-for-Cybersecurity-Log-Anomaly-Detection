from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import joblib
import os
import io
import pandas as pd
from typing import List, Any
import numpy as np

from preprocess import preprocess_input, COLUMNS
from utils import log_prediction

app = FastAPI(title="MLOps Prediction Service")

# Load models on startup
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model_v1.pkl")
PREPROCESSOR_PATH = os.path.join(MODEL_DIR, "preprocessor.pkl")

try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    print("Models loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")
    model = None
    preprocessor = None

class PredictionRequest(BaseModel):
    features: List[Any]

@app.post("/predict")
def predict(request: PredictionRequest):
    if not model or not preprocessor:
        raise HTTPException(status_code=500, detail="Models not loaded")
        
    features = request.features
    if len(features) != len(COLUMNS):
        raise HTTPException(status_code=400, detail=f"Expected {len(COLUMNS)} features, got {len(features)}")
        
    try:
        X_p = preprocess_input(features, preprocessor)
        y_pred_raw = model.predict(X_p)
        # Convert IF outputs (-1 anomaly, 1 normal) to (1 anomaly, 0 normal)
        anomaly = 1 if y_pred_raw[0] == -1 else 0
        
        log_prediction(features, anomaly)
        
        return {"anomaly": anomaly}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict_batch")
async def predict_batch(file: UploadFile = File(...)):
    """Accepts a CSV file of features without headers and predicts for each row."""
    if not model or not preprocessor:
        raise HTTPException(status_code=500, detail="Models not loaded")
        
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')), header=None)
        
        # If the user uploaded a file with more columns (e.g. including labels), truncate to 41.
        if df.shape[1] > len(COLUMNS):
            df = df.iloc[:, :len(COLUMNS)]
            
        # If it has fewer columns, it's invalid
        if df.shape[1] < len(COLUMNS):
            raise HTTPException(status_code=400, detail=f"Expected at least {len(COLUMNS)} features, got {df.shape[1]}")
            
        df.columns = COLUMNS
        
        X_p = preprocessor.transform(df)
        y_pred_raw = model.predict(X_p)
        anomalies = np.where(y_pred_raw == -1, 1, 0).tolist()
        
        # Log all predictions
        for idx, row in df.iterrows():
            log_prediction(row.tolist(), anomalies[idx])
            
        return {"predictions": anomalies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
