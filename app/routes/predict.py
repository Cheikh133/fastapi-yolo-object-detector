"""
app/routes/predict.py

Defines the /predict endpoint for YOLOv5 object detection via FastAPI.
"""
import io
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.services.inference import run_inference_on_image

router = APIRouter()


@router.post(
    "/",
    response_class=StreamingResponse,
    summary="Run object detection on an uploaded image",
)
async def predict_image(
    file: UploadFile = File(...),
    confidence: float = Query(
        0.50,
        ge=0.0,
        le=1.0,
        description="Confidence threshold for filtering detections",
    ),
) -> StreamingResponse:
    """
    Receive an image file, perform YOLOv5 inference with the specified
    confidence threshold, and return the annotated image as JPEG.

    Args:
        file: Uploaded image file in multipart/form-data.
        confidence: Float between 0.0 and 1.0 to filter out low-confidence detections.

    Returns:
        StreamingResponse: JPEG image with bounding boxes drawn.
    """
    image_bytes = await file.read()

    try:
        annotated = run_inference_on_image(image_bytes, conf_threshold=confidence)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    buffer = io.BytesIO()
    annotated.save(buffer, format="JPEG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/jpeg")
