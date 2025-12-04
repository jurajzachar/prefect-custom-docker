# Use an official Python image as the base
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl && apt-get clean

# Copy the dependency files
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/. /app

# Ensure Python finds the package and run as module
ENV PYTHONPATH=/app

# Default to running the Prefect flow
# This can be overridden by the work pool configuration
CMD ["python", "-m", "prefect_custom_docker.proxy"]