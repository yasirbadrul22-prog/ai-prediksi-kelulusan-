
from fastapi import FastAPI, HTTPException

app = FastAPI(title="AI Prediksi Kelulusan", version="1.0.0")


@app.get("/")
def home():
    return {"status": "API aktif"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/v1/prediksi/{nilai}")
def prediksi_v1(nilai: int):
    if not 0 <= nilai <= 100:
        raise HTTPException(
            status_code=400,
            detail="Nilai harus antara 0 dan 100"
        )

    return {
        "nilai": nilai,
        "prediksi": "Lulus" if nilai >= 75 else "Belum Lulus",
        "version": "1.0.0"
    }


# Endpoint lama tetap dipertahankan
@app.get("/prediksi/{nilai}")
def prediksi_lama(nilai: int):
    return prediksi_v1(nilai)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="AI Prediksi Kelulusan",
    version="1.0.0"
)


class PrediksiResponse(BaseModel):
    nilai: int
    prediksi: str
    version: str


@app.get("/")
def home():
    return {"status": "API aktif"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }


def proses_prediksi(nilai: int):
    if not 0 <= nilai <= 100:
        raise HTTPException(
            status_code=400,
            detail="Nilai harus antara 0 dan 100"
        )

    return {
        "nilai": nilai,
        "prediksi": "Lulus" if nilai >= 75 else "Belum Lulus",
        "version": "1.0.0"
    }


@app.get(
    "/v1/prediksi/{nilai}",
    response_model=PrediksiResponse
)
def prediksi_v1(nilai: int):
    return proses_prediksi(nilai)


@app.get("/prediksi/{nilai}")
def prediksi_lama(nilai: int):
    return proses_prediksi(nilai)
