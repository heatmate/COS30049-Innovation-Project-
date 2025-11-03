from fastapi import FastAPI, HTTPException, Request, BackgroundTasks, Depends
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import time
import joblib
import os 
from src.prediction import predict_vulnerability
from src.visualization import generate_visualizations, generate_distribution_chart
from fastapi.middleware.cors import CORSMiddleware

# Initialise the FastAPI application
app = FastAPI(title="Software Vulnerability Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

# Path configurations 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLOTS_DIR = os.path.join(BASE_DIR, "plots")

# Lets Input the prediction model
