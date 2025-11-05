from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import shutil
from ai_model import AIDeepfakeDetector

app = FastAPI(title="Generative AI Call Guard")

# CORS middleware (after app is defined)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Change or use ["*"] during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize your model/detector
detector = AIDeepfakeDetector()

# Folder to save uploaded audio
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Generative AI Call Guard Backend is running"}

@app.post("/detect")
async def detect_audio(file: UploadFile = File(...)):
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Run prediction
    result = detector.predict(file_path)
    return {"filename": file.filename,"result": result}