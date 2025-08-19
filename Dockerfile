# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set work directory
WORKDIR /classify.py

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI default port 
EXPOSE 8000

# Run the app FastAPI
CMD ["fastapi", "run", "classify.py", "--host", "0.0.0.0", "--port", "8000"]
