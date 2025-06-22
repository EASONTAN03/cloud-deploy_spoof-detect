FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install required system libraries for OpenCV and YOLO
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ ./app

# Set default run command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
