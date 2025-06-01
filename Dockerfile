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
      libgl1 libglib2.0-0 ffmpeg python3-tk \
      libqt5gui5 libqt5core5a libqt5widgets5 libxcb-icccm4 \
      libxcb-image0 libxcb-keysyms1 libxcb-render-util0 \
      libxcb-randr0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0 \
      libxkbcommon-x11-0 libfontconfig1 libdbus-1-3 \
 && rm -rf /var/lib/apt/lists/*

ENV QT_X11_NO_MITSHM=1
ENV QT_DEBUG_PLUGINS=1
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
ENV QT_QPA_PLATFORM=xcb

COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir \
        --no-index \
        --find-links=/wheels \
        -r requirements.txt

COPY ./*.py /app/
COPY ./*.pt /app/
COPY ./*.png /app/
COPY ./*.jpg /app/

COPY ./data/ /app/data/
COPY ./runs/ /app/runs/

WORKDIR /app

CMD ["python", "main.py"]


