FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies with retry mechanism
COPY requirements.txt .
RUN pip install --no-cache-dir --retries 3 --timeout 300 -r requirements.txt

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p output

# Set environment variables for CPU-only execution
ENV CUDA_VISIBLE_DEVICES=""
ENV TOKENIZERS_PARALLELISM=false

# Run the application
CMD ["python", "extractor_1b.py"]
