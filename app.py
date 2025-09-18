from fastapi import FastAPI, UploadFile, File, HTTPException
from models.api import ClassifyResponse
from service.orchestrate import classify_and_split
from core.config import settings

app = FastAPI(title="Classifier + Splitter Service")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/classify", response_model=ClassifyResponse)
async def classify(file: UploadFile = File(...)):
    if file.content_type not in {"application/pdf"}:
        raise HTTPException(400, "Please upload a PDF.")

    if not settings.AZ_DI_ENDPOINT or not settings.AZ_DI_KEY or not settings.DI_CLASSIFIER_MODEL_ID:
        raise HTTPException(500, "Missing Azure DI config. Fill your .env.")

    pdf = await file.read()
    result = classify_and_split(pdf)
    return result