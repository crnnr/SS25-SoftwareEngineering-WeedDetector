# Weed Detector

A computer vision application to detect weeds in agricultural settings using YOLOv8.

## Setup

1. Build the Docker container:
   ```
   docker build -t weed-detector .
   ```

2. Run the application:
   ```
   docker run --device /dev/video0:/dev/video0 --net=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix weed-detector
   ```

## Training Your Own Weed Detection Model

1. Create a dataset with labeled images of weeds and crops
2. Organize your dataset structure:
   ```
   data/
   ├── images/
   │   ├── train/
   │   │   └── images/  # Training images
   │   └── val/
   │       └── images/  # Validation images
   └── labels/
       ├── train/  # Training labels (YOLO format)
       └── val/    # Validation labels (YOLO format)
   ```

3. Copy the template file `data/data.yaml.template` to `data/data.yaml` and customize it for your dataset

4. Run the training script:
   ```
   python train.py
   ```

5. The trained model will be saved at `runs/detect_train/weights/best.pt`

6. Restart the application to use your new model

## Reference

- YOLOv8: https://github.com/ultralytics/ultralytics
- For more information, see [Ultralytics Documentation](https://docs.ultralytics.com/)
