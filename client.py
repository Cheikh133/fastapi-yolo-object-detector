"""
client.py

Batch-send images to the YOLOv5 inference API and save annotated results.
"""

import os
from pathlib import Path

import requests


API_URL: str = "http://127.0.0.1:8000/predict"
INPUT_DIR: Path = Path("images/input")
OUTPUT_DIR: Path = Path("images/output")
CONFIDENCE: float = 0.50  # default confidence threshold


def send_image(image_path: Path) -> None:
    """
    Send one image to the API with the configured confidence threshold
    and save the annotated response to disk.

    Args:
        image_path: Path to the input image file.
    """
    output_path: Path = OUTPUT_DIR / f"annotated_{image_path.name}"
    url: str = f"{API_URL}/?confidence={CONFIDENCE}"

    with image_path.open("rb") as img_file:
        response = requests.post(
            url,
            files={"file": (image_path.name, img_file, "image/jpeg")},
            stream=True,
        )

    if response.status_code == 200:
        with output_path.open("wb") as out_file:
            for chunk in response.iter_content(chunk_size=1024):
                out_file.write(chunk)
        print(f"[OK] {image_path.name} → {output_path}")
    else:
        print(
            f"[ERROR] {image_path.name} returned "
            f"{response.status_code}: {response.text}"
        )


def main() -> None:
    """
    Iterate over images in INPUT_DIR and process each one.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for img_path in INPUT_DIR.iterdir():
        if img_path.suffix.lower() in {".jpg", ".jpeg", ".png"}:
            send_image(img_path)


if __name__ == "__main__":
    main()
