from ultralytics import YOLO
import sys
from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).parent.resolve()
DATA_YAML = PROJECT_ROOT / "data" / "data.yaml"

if not DATA_YAML.exists():
    print(f"data.yaml not found at {DATA_YAML}. Please ensure your Roboflow export is correct.")
    sys.exit(1)

with open(DATA_YAML) as f:
    data_cfg = yaml.safe_load(f)
print(f"Loaded data config: {data_cfg}")

resp = input("Start YOLOv8 detection training now? (y/n): ").strip().lower()
if resp == "y":
    model = YOLO("yolov8n.pt")
    model.train(
        data=str(DATA_YAML),
        epochs=100,
        imgsz=640,
        project=str(PROJECT_ROOT / "runs"),
        name="detect_train",
        exist_ok=True,
        patience=15,
        batch=32,
        device=0
    )
    print("\nTraining complete. Check runs/detect_train/ for results.")
else:
    print("Exiting without training.")
    sys.exit(0)
