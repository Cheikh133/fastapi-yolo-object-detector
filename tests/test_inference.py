import io
import os
import pytest
from PIL import Image
from app.services.inference import run_inference_on_image


@pytest.mark.skipif(os.environ.get("CI") == "true", reason="Skip inference test in CI environment")
def test_inference_on_valid_image(fixtures_dir):
    """
    Test that inference on a valid image returns a PIL RGB image.
    """
    img_path = fixtures_dir / "sample_image.png"
    img_bytes = img_path.read_bytes()

    result = run_inference_on_image(img_bytes)
    assert isinstance(result, Image.Image)
    assert result.mode == "RGB"


@pytest.mark.skipif(os.environ.get("CI") == "true", reason="Skip inference test in CI environment")
def test_inference_on_invalid_bytes():
    """
    Test that inference with invalid bytes raises an exception.
    """
    with pytest.raises(Exception):
        run_inference_on_image(b"not an image")
