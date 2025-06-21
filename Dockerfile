FROM python:3.13-slim AS builder

WORKDIR /wheels

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip==25.1.1 --no-cache-dir \
 && pip wheel --no-cache-dir --wheel-dir . -r requirements.txt

FROM python:3.13-slim AS runtime

WORKDIR /app

# disable DL3008 (apt versions pinning) for this RUN
# hadolint ignore=DL3008
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      libgl1 \
      libglib2.0-0 \
      ffmpeg \
      python3-tk \
      libqt5gui5 \
      libqt5core5a \
      libqt5widgets5 \
      libxcb-icccm4 \
      libxcb-image0 \ 
      libxcb-keysyms1 \
      libxcb-render-util0 \
      libxcb-randr0 \
      libxcb-xinerama0 \
      libxcb-xkb1 \
      libxkbcommon-x11-0 \
      libfontconfig1 libdbus-1-3 \
      v4l-utils libv4l-dev \
      && rm -rf /var/lib/apt/lists/*

ENV QT_X11_NO_MITSHM=1
ENV QT_DEBUG_PLUGINS=1
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
ENV QT_QPA_PLATFORM=xcb
ENV OPENCV_VIDEOIO_PRIORITY_V4L2=0
ENV YOLO_CONFIG_DIR=/tmp
ENV OPENCV_VIDEOIO_DEBUG=1

COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache-dir \
        --no-index \
        --find-links=/wheels \
        -r requirements.txt

COPY ./app/*.py /app/
COPY ./*.pt /app/
COPY ./*.png /app/
COPY ./*.jpg /app/

COPY ./data/ /app/data/
COPY ./runs/ /app/runs/

WORKDIR /app

CMD ["python", "main.py"]


