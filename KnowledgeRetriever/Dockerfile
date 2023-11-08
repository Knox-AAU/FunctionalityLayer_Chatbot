# LÆS README FOR AT FORSTÅ DOCKERFILEN

FROM ubuntu:latest
FROM python:3.11

LABEL authors="Borup, Ilum, Chsten"

# Set the working directory in the container
WORKDIR /knowledge_retriever

COPY . /knowledge_retriever

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the application will listen
EXPOSE 5001

# Set the entrypoint command to run the knowledge_retriever.py file
CMD ["python", "knowledge_retriever.py"]
