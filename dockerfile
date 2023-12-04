# Stage 1: Build Python and install requirements
FROM mcr.microsoft.com/dotnet/framework/runtime:4.8-windowsservercore-ltsc2019 AS builder

# Install Python and dependencies for building
ENV PYTHON_VERSION 3.9.0
RUN curl -O https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe && \
    python-%PYTHON_VERSION%-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 && \
    del python-%PYTHON_VERSION%-amd64.exe

# Set up environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    PIP_NO_CACHE_DIR=off

# Copy your application code to the container
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Create the runtime image
FROM mcr.microsoft.com/dotnet/framework/runtime:4.8-windowsservercore-ltsc2019

# Copy Python installation from the builder stage
COPY --from=builder ["C:/Python39", "C:/Python39"]

# Copy your application code to the container
WORKDIR /app
COPY . .

# Set the command to run your application
CMD ["C:/Python39/python.exe", "main.py"]

# Metadata and labels
LABEL maintainer="Your Name <your@email.com>"
LABEL description="Description of your application"
LABEL version="1.0"
