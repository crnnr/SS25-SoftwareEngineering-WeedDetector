# syntax=docker/dockerfile:1.4

FROM python:3.10-slim AS builder

WORKDIR /wheels

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip \
 && pip wheel --no-cache-dir --wheel-dir . -r requirements.txt

FROM python:3.10-slim AS runtime

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      libgl1 libglib2.0-0 ffmpeg \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir \
        --no-index \
        --find-links=/wheels \
        -r requirements.txt

COPY ./*.py /app/
COPY ./*.pt /app/
COPY install.sh /app/

CMD ["python", "main.py"]


