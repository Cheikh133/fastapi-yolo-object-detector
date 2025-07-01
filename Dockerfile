FROM python:3.11-slim

WORKDIR /app

# Install system libraries required by OpenCV
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
       libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and assets
COPY app/ app/
COPY client.py .
COPY images/ images/
COPY notebooks/ notebooks/
COPY screenshots/ screenshots/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
