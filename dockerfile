# Use the official Python image
FROM python:3.13-slim

# Set the working directory and expose the port
EXPOSE 8000
WORKDIR /app

# Install the required packages
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the files
COPY ./app/src ./src
COPY ./app/public ./public
COPY ./app/static ./static
COPY ./app/templates ./templates
COPY ./.env ./.env

# Create the upload directory
RUN mkdir ./upload

# Remove the team.json file if it exists (this will be created by the app on first visit of the team page)
RUN rm -f -- team.json

# Run the app
CMD ["uvicorn", "src.main:app", "--port", "8000", "--host", "0.0.0.0"]
