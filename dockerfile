# Stage 1: Build Python and install requirements
FROM mcr.microsoft.com/windows/servercore:ltsc2019 AS builder

# Use PowerShell to install Python
SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]

# Download and install Python
ENV PYTHON_VERSION 3.9.0
RUN Invoke-WebRequest -Uri https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe -OutFile python-installer.exe && \
    Start-Process -Wait -FilePath python-installer.exe -ArgumentList '/quiet', 'InstallAllUsers=1', 'PrependPath=1' && \
    Remove-Item python-installer.exe -Force

# Set up environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING UTF-8
ENV PIP_NO_CACHE_DIR off

# Copy your application code to the container
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Create the runtime image
FROM mcr.microsoft.com/windows/servercore:ltsc2019

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
