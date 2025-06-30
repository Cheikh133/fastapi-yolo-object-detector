"""
app/main.py

FastAPI application entrypoint for the YOLOv5 Object Detection API.
"""
from fastapi import FastAPI

from app.routes.predict import router as predict_router

app = FastAPI(
    title="Object Detection API",
    description="Serve YOLOv5 inference via FastAPI",
    version="0.1.0",
)


@app.get("/", summary="Health Check")
async def root() -> dict[str, str]:
    """
    Health-check endpoint.

    Returns:
        A simple status message confirming the API is running.
    """
    return {"message": "API is up and running"}


app.include_router(
    predict_router,
    prefix="/predict",
    tags=["predict"],
)
