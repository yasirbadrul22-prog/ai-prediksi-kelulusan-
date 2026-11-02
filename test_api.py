
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

def test_error_nilai_di_bawah_batas():
    response = client.get("/v1/prediksi/-1")

    assert response.status_code == 400
    data = response.json()

    assert data["error"] == "Request Error"
    assert data["status_code"] == 400


def test_error_nilai_di_atas_batas():
    response = client.get("/v1/prediksi/101")

    assert response.status_code == 400
    data = response.json()

    assert data["error"] == "Request Error"
    assert data["status_code"] == 400


def test_error_endpoint_tidak_ditemukan():
    response = client.get("/alamat-tidak-ada")

    assert response.status_code == 404
    data = response.json()

    assert data["error"] == "Request Error"
    assert data["status_code"] == 404
def test_input_huruf_ditolak():
    response = client.get("/v1/prediksi/abc")

    assert response.status_code == 422

    data = response.json()
    assert data["error"] == "Validation Error"
    assert data["status_code"] == 422
def test_header_waktu_respons():
    response = client.get("/v1/prediksi/80")

    assert response.status_code == 200
    assert "X-Process-Time" in response.headers

    waktu = response.headers["X-Process-Time"]
    angka_waktu = float(waktu.replace(" ms", ""))

    assert angka_waktu >= 0
def test_cors_diizinkan():
    origin = "https://ai-prediksi-kelulusan.vercel.app/"

    response = client.options(
        "/v1/prediksi/80",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "GET"
        }
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin
def test_prediksi_v2():
    response = client.get("/v2/prediksi/80")

    assert response.status_code == 200

    data = response.json()

    assert data["nilai"] == 80
    assert data["prediksi"] == "Lulus"
    assert data["version"] == "2.0.0"
    assert "pesan" in data
def test_endpoint_lama_masih_berfungsi():
    response = client.get("/prediksi/80")

    assert response.status_code == 200
    assert response.json()["prediksi"] == "Lulus"
def test_dokumentasi_api():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    data = response.json()

    assert data["info"]["title"] == "AI Prediksi Kelulusan"
    assert data["info"]["version"] == "2.0.0"
    assert "/v2/prediksi/{nilai}" in data["paths"]

