# Use the official Python image from the Docker Hub.
FROM python:3.12-slim
LABEL authors="Ilum"

# Set the working directory in the container to /spaCy.
WORKDIR /api_connections
# Copy the current directory (The directory containing the Dockerfile) into the container at /spaCy.
COPY . /api_connections

# Install the Python dependencies.
RUN pip install -r requirements.txt

# Expose port 5000 for the Flask app to run on.
EXPOSE 5002
# Define the command that will be executed when the Docker container starts.
CMD ["python", "database_API.py"]

#Run unittests
#RUN python -m unittest spaCyTests.py