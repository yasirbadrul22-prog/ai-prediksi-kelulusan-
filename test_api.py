
import requests
import csv
import time
from datetime import datetime, timezone

BASE_URL = "https://ai-prediksi-kelulusan.vercel.app"
ENDPOINT = BASE_URL + "/prediksi/80"

JUMLAH_UJI = 5
catatan = []

for nomor in range(1, JUMLAH_UJI + 1):
    mulai = time.perf_counter()

    try:
        response = requests.get(ENDPOINT, timeout=20)
        durasi = round(time.perf_counter() - mulai, 3)

        catatan.append({
            "percobaan": nomor,
            "waktu_utc": datetime.now(timezone.utc).isoformat(),
            "status_http": response.status_code,
            "durasi_detik": durasi,
            "berhasil_http": 200 <= response.status_code < 300,
            "detail": response.text[:100].replace("\n", " ")
        })

    except requests.RequestException as error:
        durasi = round(time.perf_counter() - mulai, 3)

        catatan.append({
            "percobaan": nomor,
            "waktu_utc": datetime.now(timezone.utc).isoformat(),
            "status_http": "",
            "durasi_detik": durasi,
            "berhasil_http": False,
            "detail": str(error)[:100]
        })

total = len(catatan)
berhasil = sum(1 for item in catatan if item["berhasil_http"])
gagal = total - berhasil
persen = round(berhasil / total * 100, 1) if total else 0

print("=== Ringkasan Pemantauan API ===")
print("Total permintaan:", total)
print("Respons HTTP sukses:", berhasil)
print("Gagal atau non-2xx:", gagal)
print("Tingkat keberhasilan HTTP:", persen, "%")

with open("laporan_hari65.csv", "w", newline="", encoding="utf-8") as file:
    kolom = [
        "percobaan", "waktu_utc", "status_http",
        "durasi_detik", "berhasil_http", "detail"
    ]
    writer = csv.DictWriter(file, fieldnames=kolom)
    writer.writeheader()
    writer.writerows(catatan)

print("File laporan tersimpan: laporan_hari65.csv")
import os
import time
import requests

BASE_URL = os.environ["API_BASE_URL"].rstrip("/")

def test_api_merespons_dalam_batas_waktu():
    mulai = time.perf_counter()

    response = requests.get(
        BASE_URL + "/prediksi/80",
        timeout=20
    )

    durasi = time.perf_counter() - mulai

    assert response.status_code == 200
    assert durasi < 10, (
        f"Respons terlalu lambat: {durasi:.2f} detik"
    )
import os
import requests

BASE_URL = os.environ["API_BASE_URL"].rstrip("/")

def test_nilai_batas_bawah():
    response = requests.get(
        BASE_URL + "/prediksi/0",
        timeout=20
    )
    assert response.status_code == 200

def test_nilai_batas_atas():
    response = requests.get(
        BASE_URL + "/prediksi/100",
        timeout=20
    )
    assert response.status_code == 200
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
def test_struktur_json_prediksi():
    response = requests.get(
        BASE_URL + "/prediksi/80",
        timeout=20
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert "prediksi" in data
import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL")

def test_api_berjalan():
    assert API_BASE_URL, "API_BASE_URL belum diatur"

    response = requests.get(API_BASE_URL, timeout=20)

    assert response.status_code == 200
- name: Jalankan tes API
  env:
    API_BASE_URL: ${{ secrets.API_BASE_URL }}
  run: pytest -v