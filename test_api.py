
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
