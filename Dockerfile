# Single-Cell RNA-seq Analysis Pipeline
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY single_cell_analysis.py .
COPY download_data.py .

# Create necessary directories
RUN mkdir -p data/raw results/single_cell_analysis/figures

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV NUMBA_CACHE_DIR=/tmp

# Run the pipeline
CMD ["sh", "-c", "python download_data.py && python single_cell_analysis.py"]
