# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the app FastAPI
CMD ["python", "app:app", "--host", "0.0.0.0", "--port", "8000"]
