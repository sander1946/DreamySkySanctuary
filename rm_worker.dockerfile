# Use the official Python image
FROM python:3.13-slim

# Set the working directory and expose the port
WORKDIR /app

# Install the required packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the app
CMD ["python", "rm_worker.py"]
