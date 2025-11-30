
# Use official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies for pandas/pyarrow
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file from repo root
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code from service folder
COPY . .

# Cloud Run expects port 8080
EXPOSE 8080

# Environment variables for GCP and app config
ENV PORT=8080 \
    GOOGLE_APPLICATION_CREDENTIALS="/app/credentials.json" \
    GCP_BUCKET_NAME="e2e-ml-ops" \
    GCP_DATASET="e2e_mlops_schema" \
    GCP_TABLE="states_parquet"

# Run Flask app
CMD ["python", "-m", "service.main"]
