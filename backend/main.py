from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import re
import pandas as pd
import os

# Initialize FastAPI app
app = FastAPI(
    title="Phishing URL Detector API",
    description="API for detecting phishing URLs using machine learning",
    version="1.0.0"
)

# Enable CORS (so frontend can communicate with backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class URLRequest(BaseModel):
    url: str

# Response model
class PredictionResponse(BaseModel):
    url: str
    prediction: str  # "Safe" or "Phishing"
    confidence: float
    features: dict

# Feature extraction function (same as training)
def extract_features(url: str) -> dict:
    features = {}
    features['length'] = len(url)
    features['has_at'] = 1 if '@' in url else 0
    features['has_ip'] = 1 if re.match(r'\d+\.\d+\.\d+\.\d+', url) else 0
    features['https'] = 1 if url.startswith('https') else 0
    features['num_dots'] = url.count('.')
    features['num_hyphens'] = url.count('-')
    features['num_slashes'] = url.count('/')
    features['num_digits'] = sum(c.isdigit() for c in url)
    return features

# Load the model (do this once at startup)
model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'phishing_model.pkl')
try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Phishing URL Detector API",
        "docs": "/docs"
    }

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
def predict_url(request: URLRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Extract features
        features = extract_features(request.url)
        
        # Convert to DataFrame (same format as training)
        features_df = pd.DataFrame([features])
        
        # Make prediction
        prediction = model.predict(features_df)[0]
        prediction_proba = model.predict_proba(features_df)[0]
        
        # Get confidence score
        confidence = float(max(prediction_proba) * 100)
        
        # Convert prediction to label
        prediction_label = "Phishing" if prediction == 1 else "Safe"
        
        return PredictionResponse(
            url=request.url,
            prediction=prediction_label,
            confidence=round(confidence, 2),
            features=features
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)