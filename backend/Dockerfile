FROM python:3.11-slim

ARG SERVICE_NAME

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy service-specific files
COPY ${SERVICE_NAME} /${SERVICE_NAME}
COPY common /app/common
COPY config /app/config

# Create non-root user
RUN useradd -m appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose service port (will be overridden by environment variable)
EXPOSE 8000

# Set default command
CMD ["python", "-m", "${SERVICE_NAME}.app"]

