import io
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_predict_route_with_valid_image(fixtures_dir):
    img_path = fixtures_dir / "sample_image.png"
    with open(img_path, "rb") as f:
        response = client.post(
            "/predict/",
            files={"file": ("sample.png", f, "image/png")},
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    assert response.content  # non-empty body


def test_predict_route_with_invalid_file():
    # Send a text payload => expect 422 or 500
    response = client.post(
        "/predict/",
        files={"file": ("test.txt", io.BytesIO(b"hello"), "text/plain")},
    )
    assert response.status_code in (422, 500)