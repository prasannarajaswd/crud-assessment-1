# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies for psycopg2-binary
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables
ENV FLASK_DEBUG=1
ENV SECRET_KEY=your_secret_key
ENV DATABASE_URL=postgresql://user:password@db/dbname

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
