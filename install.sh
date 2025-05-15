#!/bin/bash
set -e

pip install --no-cache-dir -r /app/requirements.txt
python3 /app/main.py
