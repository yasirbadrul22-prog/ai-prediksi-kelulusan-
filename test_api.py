
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

def test_nilai_tepat_batas_lulus():
    response = client.get("/prediksi/75")

    assert response.status_code == 200
    assert response.json()["prediksi"] == "Lulus"


def test_nilai_satu_di_bawah_batas():
    response = client.get("/prediksi/74")

    assert response.status_code == 200
    assert response.json()["prediksi"] == "Belum Lulus"

def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_prediksi_v1():
    response = client.get("/v1/prediksi/80")

    assert response.status_code == 200
    assert response.json()["prediksi"] == "Lulus"
    assert response.json()["version"] == "1.0.0"


def test_endpoint_lama():
    response = client.get("/prediksi/80")

    assert response.status_code == 200
    assert response.json()["prediksi"] == "Lulus"
def test_struktur_respons_prediksi():
    response = client.get("/v1/prediksi/80")
    data = response.json()

    assert response.status_code == 200
    assert "nilai" in data
    assert "prediksi" in data
    assert "version" in data


def test_tipe_data_respons_prediksi():
    response = client.get("/v1/prediksi/80")
    data = response.json()

    assert isinstance(data["nilai"], int)
    assert isinstance(data["prediksi"], str)
    assert isinstance(data["version"], str)


def test_respons_prediksi_nilai_60():
    response = client.get("/v1/prediksi/60")
    data = response.json()

    assert response.status_code == 200
    assert data["prediksi"] == "Belum Lulus"


