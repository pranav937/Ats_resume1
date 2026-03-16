# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Tesseract OCR and OpenCV/FitZ
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create output and resumes directory if they don't exist
RUN mkdir -p output resumes

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Command to run the FastAPI server
# Render/Railway usually expect one health check port. 
# We'll run uvicorn on 8000 as the primary entry point.
CMD ["uvicorn", "api.py:app", "--host", "0.0.0.0", "--port", "8000"]
