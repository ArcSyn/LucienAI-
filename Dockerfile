FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash lucien && \
    chown -R lucien:lucien /app
USER lucien

# Expose port (if needed for future web interface)
EXPOSE 8000

# Default command
CMD ["python", "Lucien.py"]
