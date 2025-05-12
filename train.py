import random
import shutil
import yaml
import sys
from pathlib import Path
from ultralytics import YOLO

PROJECT_ROOT = Path(__file__).parent.resolve()
SRC_DIR      = PROJECT_ROOT / "data"
TRAIN_DIR    = SRC_DIR / "train"
VAL_DIR      = SRC_DIR / "val"
YAML_FILE    = PROJECT_ROOT / "data.yaml"

for d in (TRAIN_DIR, VAL_DIR):
    d.mkdir(parents=True, exist_ok=True)

classes = [
    d for d in SRC_DIR.iterdir()
    if d.is_dir() and d.name.lower() not in ("train", "val")
]

for class_dir in classes:
    imgs = list(class_dir.glob("*.*"))
    random.shuffle(imgs)
    split_idx = int(0.8 * len(imgs))

    for i, img_path in enumerate(imgs):
        dest_root = TRAIN_DIR if i < split_idx else VAL_DIR
        out_dir    = dest_root / class_dir.name
        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(img_path, out_dir / img_path.name)
        print(f"Copied {img_path.name} → {out_dir}")

print(f"\nDone splitting into:\n  {TRAIN_DIR}\n  {VAL_DIR}\n")

class_names = sorted([d.name for d in classes])
data_cfg = {
    "train": str(TRAIN_DIR.resolve()),
    "val":   str(VAL_DIR.resolve()),
    "nc":    len(class_names),
    "names": class_names
}

with open(YAML_FILE, "w") as f:
    yaml.dump(data_cfg, f, default_flow_style=False)

print(f"Generated {YAML_FILE} with classes: {class_names}\n")

# ——— 5. Prompt user & run training ———
resp = input("Start YOLOv8 classification training now? (y/n): ").strip().lower()
if resp == "y":
    model = YOLO("yolov8n-cls.pt")
    model.train(
        data=str(SRC_DIR.resolve()),
        epochs=50,
        imgsz=640,
        project=str(PROJECT_ROOT / "runs"),
        name="classify_train",
        exist_ok=True
    )
    print("\nTraining complete. Check runs/classify_train/ for results.")
else:
    print("Exiting without training.")
    sys.exit(0)
