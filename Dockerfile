FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, and system dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-tk libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip

# Set up app directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt

# Copy your code
COPY ./*.py /app/
COPY ./*.pt /app/
COPY install.sh /app/
RUN chmod +x /app/install.sh

ENTRYPOINT ["/app/install.sh"]