# Use the official Python image
FROM python:3.13-slim

# Set the working directory and expose the port
EXPOSE 80
WORKDIR /app

# Install the required packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the app
CMD ["uvicorn", "src.main:app", "--port", "80", "--host", "0.0.0.0", "--reload"]
