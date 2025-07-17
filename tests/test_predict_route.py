import io
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.skipif(os.environ.get("CI") == "true", reason="Skip endpoint test in CI")
def test_predict_route_with_valid_image(fixtures_dir):
    """
    Test the /predict/ endpoint with a valid image.
    This test is skipped in CI because the model is not loaded in that environment.
    """
    img_path = fixtures_dir / "sample_image.png"
    with open(img_path, "rb") as f:
        response = client.post(
            "/predict/",
            files={"file": ("sample.png", f, "image/png")},
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    assert response.content  # ensure response body is not empty


@pytest.mark.skipif(os.environ.get("CI") == "true", reason="Skip endpoint test in CI")
def test_predict_route_with_invalid_file():
    """
    Test the /predict/ endpoint with an invalid file format.
    Should return 422 or 500 depending on validation or inference failure.
    """
    response = client.post(
        "/predict/",
        files={"file": ("test.txt", io.BytesIO(b"hello"), "text/plain")},
    )
    assert response.status_code in (422, 500)
