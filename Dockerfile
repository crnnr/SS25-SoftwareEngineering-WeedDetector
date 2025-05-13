FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

COPY ./*.py /app/
COPY ./*.pt /app/
COPY install.sh /app/

WORKDIR /app

RUN chmod +x /app/install.sh

ENTRYPOINT ["bash","/app/install.sh"]