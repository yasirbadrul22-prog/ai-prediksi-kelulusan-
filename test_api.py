
import os
import requests


BASE_URL = os.environ["API_BASE_URL"].rstrip("/")


def test_endpoint_utama():
    response = requests.get(BASE_URL + "/", timeout=20)
    assert response.status_code == 200


def test_prediksi_lulus():
    response = requests.get(BASE_URL + "/prediksi/80", timeout=20)
    assert response.status_code == 200
    assert "Lulus" in response.text
    assert "Belum Lulus" not in response.text


def test_prediksi_belum_lulus():
    response = requests.get(BASE_URL + "/prediksi/60", timeout=20)
    assert response.status_code == 200
    assert "Belum Lulus" in response.text


def test_nilai_di_luar_rentang():
    response = requests.get(BASE_URL + "/prediksi/120", timeout=20)
    assert response.status_code == 400

def test_nilai_minimum():
    response = requests.get(
        BASE_URL + "/prediksi/0", timeout=20
    )
    assert response.status_code == 200


def test_nilai_maksimum():
    response = requests.get(
        BASE_URL + "/prediksi/100", timeout=20
    )
    assert response.status_code == 200
def test_prediksi_60():
    response = requests.get(
        BASE_URL + "/prediksi/60",
        timeout=20
    )
    assert response.status_code == 200
    assert "Belum Lulus" in response.text


def test_prediksi_80():
    response = requests.get(
        BASE_URL + "/prediksi/80",
        timeout=20
    )
    assert response.status_code == 200
    assert "Lulus" in response.text
    assert "Belum Lulus" not in response.text
import requests

def uji_prediksi(nilai, hasil_diharapkan):
    response = requests.get(
        f"{BASE_URL}/prediksi/{nilai}",
        timeout=20
    )

    assert response.status_code == 200, (
        f"Status tidak sesuai: {response.status_code}"
    )

    assert hasil_diharapkan.lower() in response.text.lower(), (
        f"Hasil tidak sesuai: {response.text}"
    )

    print(f"Tes nilai {nilai}: LULUS")

uji_prediksi(60, "Belum Lulus")
uji_prediksi(80, "Lulus")

