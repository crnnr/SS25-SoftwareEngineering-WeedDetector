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
pip install --upgrade pip

pip install ultralytics opencv-python
```

## Docker

```bash
sudo docker build -t weed-detector .
xhost +local:root
sudo docker run --device /dev/video0:/dev/video0 --net=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix weed-detector
```
