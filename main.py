import logging
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException 
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="AI Prediksi Kelulusan",
    version="1.0.0"
)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(message)s"
)

logger = logging.getLogger("api_ml")

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
    logger.info("Permintaan prediksi diterima")

    if not 0 <= nilai <= 100:
        logger.warning("Nilai di luar batas: %s", nilai)
        raise HTTPException(
            status_code=400,
            detail="Nilai harus antara 0 dan 100"
        )

    hasil = {
        "nilai": nilai,
        "prediksi": "Lulus" if nilai >= 75 else "Belum Lulus",
        "version": "1.0.0"
    }

    logger.info("Prediksi berhasil diproses")
    return hasil


@app.get(
    "/v1/prediksi/{nilai}",
    response_model=PrediksiResponse
)
def prediksi_v1(nilai: int):
    return proses_prediksi(nilai)
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Request Error",
            "detail": str(exc.detail),
            "status_code": exc.status_code
        }
    )
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):


    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": "Input tidak valid. Nilai harus berupa angka.",
            "status_code": 422
        }
    )
@app.get("/prediksi/{nilai}")
def prediksi_lama(nilai: int):
    return proses_prediksi(nilai)

