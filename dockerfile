# Lightweight Python image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files.
COPY app.py .
COPY templates/ ./templates/

# It exposes the Flask door.
EXPOSE 5000

# Command to run
CMD ["python", "app.py"]