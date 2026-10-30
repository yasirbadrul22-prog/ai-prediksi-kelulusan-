
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "API aktif"}


def test_prediksi_lulus():
    response = client.get("/prediksi/80")
    assert response.status_code == 200
    assert response.json()["prediksi"] == "Lulus"


def test_prediksi_belum_lulus():
    response = client.get("/prediksi/60")
    assert response.status_code == 200
    assert response.json()["prediksi"] == "Belum Lulus"


def test_nilai_batas_bawah():
    response = client.get("/prediksi/0")
    assert response.status_code == 200


def test_nilai_batas_atas():
    response = client.get("/prediksi/100")
    assert response.status_code == 200


def test_nilai_di_luar_rentang():
    response = client.get("/prediksi/120")
    assert response.status_code == 400
