from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import pandas as pd

from backend.app.ml.feature_extraction import extract_features

app = FastAPI(title="AI-Powered Phishing Detection System")

# Load trained ML model
model = joblib.load("backend/app/ml/phishing_model.pkl")


class URLRequest(BaseModel):
    url: str


@app.get("/")
def home():
    return FileResponse("backend/app/index.html")


@app.post("/predict")
def predict(request: URLRequest):

    # Extract URL features
    features = extract_features(request.url)

    # Convert features into DataFrame
    df = pd.DataFrame([features])

    # Make ML prediction
    prediction = model.predict(df)[0]

    # Get phishing probability
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(df)[0]

        if 1 in model.classes_:
            phishing_index = list(model.classes_).index(1)
            phishing_probability = probabilities[phishing_index]
        else:
            phishing_probability = 1.0 if prediction == 1 else 0.0
    else:
        phishing_probability = 1.0 if prediction == 1 else 0.0

    # Convert probability to risk score
       
    risk_score = round(phishing_probability * 100, 2)
    confidence = round(
        (phishing_probability if prediction == 1 else 1 - phishing_probability) * 100, 2
    )
    # Decide final result
    if risk_score >= 70:
        result = "Phishing"
    elif risk_score >= 30:
        result = "Suspicious"
    else:
        result = "Legitimate"

    # Print information in terminal
    print("URL:", request.url)
    print("ML Prediction:", prediction)
    print("Phishing Probability:", phishing_probability)
    print("Risk Score:", risk_score)
    print("Final Result:", result)
    print("Features:", features)

    return {
    "url": request.url,
    "prediction": result,
    "risk_score": risk_score,
    "confidence": confidence,
    "features": features
}