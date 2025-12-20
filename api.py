from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(
    title="API Prédiction Prix Voitures Maroc",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    model = joblib.load("best_model.pkl")
except Exception:
    model = None

class VoitureFeatures(BaseModel):
    features: dict

@app.get("/")
def root():
    return {"status": "API en ligne"}

@app.get("/health")
def health():
    return {"model_loaded": model is not None}

@app.post("/predict")
def predict_price(data: VoitureFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Modèle non disponible")

    try:
        input_df = pd.DataFrame([data.features])
        prediction = model.predict(input_df)[0]
        prix_estime = max(int(round(prediction)), 10000)
        return {"prix_estime": prix_estime}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)