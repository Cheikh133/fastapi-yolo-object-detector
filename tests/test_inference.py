import io
import pytest
from PIL import Image
from app.services.inference import run_inference_on_image


def test_inference_on_valid_image(fixtures_dir):
    # Load sample image bytes
    img_path = fixtures_dir / "sample_image.png"
    img_bytes = img_path.read_bytes()

    # Should return a PIL Image
    result = run_inference_on_image(img_bytes)
    assert isinstance(result, Image.Image)
    assert result.mode == "RGB"


def test_inference_on_invalid_bytes():
    # Passing non-image bytes should raise an exception
    with pytest.raises(Exception):
        run_inference_on_image(b"not an image")