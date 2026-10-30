
import os
import requests


def test_api_berjalan():
    api_base_url = os.getenv("API_BASE_URL")

    assert api_base_url, "Secret API_BASE_URL belum diatur"

    response = requests.get(
        api_base_url.rstrip("/"),
        timeout=20
    )

    assert response.status_code == 200
import requests

BASE_URL = "https://ai-prediksi-kelulusan.vercel.app/"

def test_nilai_batas_bawah():
    response = requests.get(f"{BASE_URL}/prediksi/0")
    assert response.status_code == 200

def test_nilai_batas_atas():
    response = requests.get(f"{BASE_URL}/prediksi/100")
    assert response.status_code == 200

def test_nilai_di_luar_rentang():
    response = requests.get(f"{BASE_URL}/prediksi/120")
    assert response.status_code in (400, 422)
