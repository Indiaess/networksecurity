FROM python:3.10-slim-buster

WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install AWS CLI (latest version)
RUN pip install --no-cache-dir awscli

# Copy rest of the application
COPY . .

# Run app
CMD ["python", "app.py"]