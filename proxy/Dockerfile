# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Copy the requirements file
COPY requirements.txt /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 5006
EXPOSE 5010

# Run the proxy server
CMD ["python", "server.py"]
