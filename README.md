# Activating the Virtual Environment

## Bash / Zsh

```bash
bash
python -m venv .venv
source .venv/bin/activate
```

## Fish

```fish
python -m venv .venv
source .venv/bin/activate.fish
```

## Install Dependencies

```bash
bash ./install.sh
```

## Docker

```bash
sudo docker build -t weed-detector .
xhost +local:root
sudo docker run --device /dev/video0:/dev/video0 --net=host \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -e XDG_RUNTIME_DIR=/tmp/runtime-root \
  -e QT_QPA_PLATFORM=xcb \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  weed-detector
```
