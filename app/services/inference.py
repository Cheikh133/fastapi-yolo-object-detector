"""
app/services/inference.py

Defines the function to run YOLOv5 object detection inference.
"""
import io
from typing import Final

from PIL import Image
import torch

# Load YOLOv5 model once
model: Final[torch.nn.Module] = torch.hub.load(
    'ultralytics/yolov5', 'yolov5s', pretrained=True
)
model.eval()

# Store default confidence threshold
DEFAULT_CONF: Final[float] = model.conf


def run_inference_on_image(
    image_bytes: bytes,
    conf_threshold: float = 0.50,
) -> Image.Image:
    """
    Run YOLOv5 inference on raw image bytes with a custom confidence threshold.

    Args:
        image_bytes: Raw bytes of the input image.
        conf_threshold: Float in [0.0, 1.0] to filter weak detections.

    Returns:
        A PIL Image with bounding boxes drawn.
    """
    # Load image from bytes
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

    # Temporarily override model confidence threshold
    original_conf = model.conf
    model.conf = conf_threshold

    # Perform inference
    results = model(image)

    # Restore original threshold
    model.conf = original_conf

    # Draw boxes & labels in-place
    results.render()

    # Convert first annotated frame to PIL and return
    annotated_frame = results.ims[0]
    return Image.fromarray(annotated_frame)
