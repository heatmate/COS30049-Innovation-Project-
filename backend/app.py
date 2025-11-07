from fastapi import FastAPI, HTTPException, Request, BackgroundTasks, Depends
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import time
import joblib
import os 
from src.prediction import predict_vulnerability
from src.visualization import generate_visualizations, generate_distribution_chart
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from scipy.sparse import hstack
from src.features import clean_code, extract_features
import logging
import joblib


# Initialise logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("vulnerability_api")

# Initialise the FastAPI application
app = FastAPI(title="Software Vulnerability Detection API")

# Allow the react frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
logger.info(f"Upload directory set to: {UPLOAD_DIR}")


@app.get("/predict_v2")
def predict_vulnerability_api(code_snippet: str):
    """Predict vulnerability for a code snippet"""
    logger.info("Received code snippet for prediction.")
    
    try:
        clean = clean_code(code_snippet)
        logger.debug(f"Cleaned code: {clean[:100]}...")  # log only first 100 chars

        features = extract_features(code_snippet)
        logger.debug(f"Extracted features: {features}")
        vectorizer = joblib.load("vectorizer.pkl")

        text = vectorizer.transform([clean])
        feature_cols = ['has_user_input','has_db_operation','has_file_operation',
                        'has_eval','code_length','has_validation','has_quotes','has_concatenation']
        numerical = np.array([[features.get(c, 0) for c in feature_cols]])

        X = hstack([text, numerical])
        logger.info("Features prepared for model prediction.")
        model = joblib.load("logistic_regression.pkl")
        pred = model.predict(X)[0]
        probs = model.predict_proba(X)[0]
        logger.info(f"Prediction: {pred}, Confidence: {max(probs)}")
        encoder = joblib.load("label_encoder.pkl")
        response = {
            "vulnerability_category": encoder.inverse_transform([pred])[0],
            "confidence": max(probs),
            "probabilities": dict(zip(encoder.classes_, probs))
        }
        logger.info(f"Response prepared: {response}")
        return response

    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Prediction failed.")
