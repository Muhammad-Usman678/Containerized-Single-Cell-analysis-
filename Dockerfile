# Single-Cell RNA-seq Analysis Pipeline# Use Python 3.10 slim image

FROM python:3.11-slimFROM python:3.10-slim



# Set working directory# Set working directory

WORKDIR /appWORKDIR /app



# Install system dependencies# Install system dependencies

RUN apt-get update && apt-get install -y \RUN apt-get update && apt-get install -y \

    build-essential \    gcc \

    libhdf5-dev \    g++ \

    pkg-config \    git \

    && rm -rf /var/lib/apt/lists/*    && rm -rf /var/lib/apt/lists/*



# Copy requirements# Copy requirements

COPY requirements.txt .COPY requirements.txt .



# Install Python dependencies# Install Python dependencies

RUN pip install --no-cache-dir -r requirements.txtRUN pip install --no-cache-dir -r requirements.txt



# Copy application files# Copy application code

COPY single_cell_analysis.py .COPY src/ ./src/

COPY download_data.py .COPY models/ ./models/

COPY monitoring/ ./monitoring/

# Create necessary directories

RUN mkdir -p data/raw results/single_cell_analysis/figures# Create necessary directories

RUN mkdir -p data/processed mlruns

# Set environment variables

ENV PYTHONUNBUFFERED=1# Set environment variables

ENV NUMBA_CACHE_DIR=/tmpENV PYTHONUNBUFFERED=1

ENV MODEL_PATH=/app/models/best_model.pkl

# Run the pipeline

CMD ["sh", "-c", "python download_data.py && python single_cell_analysis.py"]# Expose API port

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
CMD ["python", "-m", "uvicorn", "src.serve:app", "--host", "0.0.0.0", "--port", "8000"]
