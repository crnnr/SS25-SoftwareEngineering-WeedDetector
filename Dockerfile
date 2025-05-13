FROM python:3.13

COPY requirements.txt /app/requirements.txt

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    pip install -r /app/requirements.txt

COPY ./*.py /app/
COPY ./*.pt /app/

WORKDIR /app

CMD ["python", "main.py"]