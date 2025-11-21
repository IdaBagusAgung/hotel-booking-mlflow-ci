# Dockerfile for ML Model Artifacts
# Author: gus_agung
# Purpose: Package trained model artifacts for deployment

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies for model serving
RUN pip install --no-cache-dir \
    mlflow==2.16.2 \
    scikit-learn \
    pandas \
    numpy \
    flask \
    joblib

# Copy model artifacts (will be created during MLflow training)
# Note: Models will be loaded from MLflow during runtime
# This copies the models directory structure
COPY models/ /app/models/

# Copy preprocessed data
COPY hotel_bookings_preprocessed/ /app/hotel_bookings_preprocessed/

# Copy training scripts
COPY modelling.py modelling_tuning.py /app/

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV MODEL_VERSION=1.0.0

# Default command
CMD ["echo", "Model artifacts packaged successfully"]
