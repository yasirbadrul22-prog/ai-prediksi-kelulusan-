
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="AI Prediksi Kelulusan",
    version="1.0.0"
)


class PrediksiResponse(BaseModel):
    nilai: int
    prediksi: str
    version: str


class ErrorResponse(BaseModel):
    error: str
    detail: str
    status_code: int


@app.exception_handler(HTTPException)
async def custom_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Request Error",
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )


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
from starlette.exceptions import HTTPException as StarletteHTTPException
@app.exception_handler(StarletteHTTPException)
@app.exception_handler(HTTPException)
