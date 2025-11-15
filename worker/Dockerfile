FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Download and extract gamedata from GitHub Releases
RUN mkdir -p /wakfu_data && \
    curl -L https://github.com/gabriel20x/wakfu-builder-assistant/releases/download/v1.0.0-gamedata/gamedata_1.90.1.43.tar.gz \
    -o /tmp/gamedata.tar.gz && \
    tar -xzf /tmp/gamedata.tar.gz -C /wakfu_data && \
    rm /tmp/gamedata.tar.gz

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Wait for database to be ready
CMD ["python", "fetch_and_load.py"]

