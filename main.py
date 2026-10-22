from fastapi import FastAPI, HTTPException

app = FastAPI(title="AI Prediksi Kelulusan")

@app.get("/")
def home():
    return {"status": "API aktif"}

@app.get("/prediksi/{nilai}")
def prediksi(nilai: int):
    if not 0 <= nilai <= 100:
        raise HTTPException(
            status_code=400,
            detail="Nilai harus antara 0 dan 100"
        )

    return {
        "nilai": nilai,
        "prediksi": "Lulus" if nilai >= 75 else "Belum Lulus"
    }