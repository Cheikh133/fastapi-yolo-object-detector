"""
app/services/inference.py

Defines the function to run YOLOv5 object detection inference.
"""

import io
import os
from typing import Final, Optional, Tuple

from PIL import Image
import torch

# Conditionally load YOLOv5 model unless in CI environment
if os.environ.get("CI") == "true":
    model: Optional[torch.nn.Module] = None
    DEFAULT_CONF: Final[float] = 0.5  # Default fallback value
else:
    model: Final[torch.nn.Module] = torch.hub.load(
        'ultralytics/yolov5', 'yolov5s', pretrained=True
    )
    model.eval()
    DEFAULT_CONF: Final[float] = model.conf


def run_inference_on_image(
    image_bytes: bytes,
    conf_threshold: float = 0.5,
) -> Image.Image:
    """
    Run YOLOv5 inference on raw image bytes with a custom confidence threshold.

    Args:
        image_bytes (bytes): Raw bytes of the input image.
        conf_threshold (float): Threshold for filtering weak detections, between 0.0 and 1.0.

    Returns:
        Image.Image: A PIL Image with bounding boxes drawn.

    Raises:
        RuntimeError: If the model is not loaded (e.g., in CI context).
    """
    if model is None:
        raise RuntimeError("Model not loaded: skipping inference in CI environment.")

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Temporarily override model confidence threshold
    original_conf = model.conf
    model.conf = conf_threshold

    # Perform inference
    results = model(image)

    # Restore original threshold
    model.conf = original_conf

    # Draw boxes & labels in-place
    results.render()

    annotated_frame = results.ims[0]
    return Image.fromarray(annotated_frame)