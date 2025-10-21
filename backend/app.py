from fastapi import FastAPI, HTTPException, Request, BackgroundTasks, Depends
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import time
import joblib
import os 
from src.prediction import predict_vulnerability
from src.visualization import 

app = FastAPI(title="Software Vulnerability Detection API")