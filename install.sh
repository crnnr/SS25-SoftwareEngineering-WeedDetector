#!/bin/bash
set -e

pip install --no-cache-dir -r /app/requirements.txt
python /app/main.py
