from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.services.inference import run_inference_on_image
import io

router = APIRouter()  # router for all /predict endpoints

@router.post("/", response_class=StreamingResponse)
async def predict_image(
    file: UploadFile = File(...)  # accept an uploaded file
):
    """
    Receive an image file, run YOLO inference, and return annotated image.
    """
    # read raw bytes from upload
    content = await file.read()

    try:
        # perform inference and get a PIL Image with bounding boxes
        annotated_image = run_inference_on_image(content)
    except Exception as e:
        # if something goes wrong, return HTTP 500
        raise HTTPException(status_code=500, detail=str(e))

    # write image bytes to a buffer
    buffer = io.BytesIO()
    annotated_image.save(buffer, format="JPEG")
    buffer.seek(0)

    # stream back the annotated image
    return StreamingResponse(buffer, media_type="image/jpeg")
