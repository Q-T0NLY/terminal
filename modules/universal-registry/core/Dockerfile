FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY advanced_main.py .
COPY static/ static/

# Expose port
EXPOSE 8000

# Run service
CMD ["uvicorn", "advanced_main:app", "--host", "0.0.0.0", "--port", "8000"]
