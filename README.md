# YOLOv5 Object Detection API

A REST API using FastAPI and YOLOv5 to detect objects in images. Includes an interactive Swagger UI and a batch client script for automated testing.


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Cheikh133/fastapi-yolo-object-detector.git
   cd fastapi-yolo-object-detector
   ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    # Windows PowerShell
    .venv\Scripts\Activate.ps1
    # macOS/Linux
    source .venv/bin/activate
    ```
3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the API

Start the server with:  

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Interactive API Documentation

Visit the Swagger UI at `http://127.0.0.1:8000/docs`

Test the `POST /predict/` endpoint directly in your browser:

![Swagger UI – POST /predict](screenshots/swagger.png)

**file**: upload an image (JPEG/PNG)  

## POST /predict/

Send an image and receive an annotated result.

- **Endpoint**: `/predict/`  
- **Method**: `POST`  
- **Request**: multipart/form-data with `file=@<image>` and optional `?confidence=0.5`  
- **Response**: JPEG image with bounding boxes  

## Batch Processing with `client.py`

Process all images in `images/input/` and save results:
```bash
python client.py
```
Annotated images are saved to `images/output/annotated_<filename>`. The default confidence threshold is 0.50.

## Demo Output

Sample detection on a daytime street scene (`annotated_pic5.png`):

![Demo Daytime Scene](images/output/pannotated_pic5.png)

## Threshold Analysis

An analysis of how the confidence threshold affects:

- Number of detections  
- Average confidence  

See `notebooks/threshold_analysis.ipynb` for details. This guided our choice of 0.50 as the default threshold.

