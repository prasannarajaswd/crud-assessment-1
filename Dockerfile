# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for psycopg2-binary
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask application
EXPOSE 5000

# Define environment variables (default values for development)
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
