# Use python as base image
FROM python

# Set the working directory in the container
WORKDIR /llama

# Copy the current directory contents into the container at /llama
COPY ./llama_cpu_server.py /llama/llama_cpu_server.py
COPY ./Llama2.gguf* /llama/Llama2.gguf

# Install the needed packages
RUN pip install llama-cpp-python
RUN pip install Flask

#Expose port 5004 outisde of the container
EXPOSE 5004

# Run llama_cpu_server.py when the container launches
CMD ["python", "llama_cpu_server.py"]