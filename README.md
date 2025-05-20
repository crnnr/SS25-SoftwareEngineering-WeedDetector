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

## Using the Default Model

The application will use the default YOLOv8n model if no trained weed detection model is found. The default model can detect standard objects like:

- Class 47: 'apple'
- Class 50: 'broccoli'
- Class 51: 'carrot'
- Class 58: 'potted plant'

These classes might be useful for general plant detection until you train a custom weed detector.

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

## Troubleshooting

If detection is not working:

1. Run the find_models.py script to locate all models and data files:
   ```
   python find_models.py
   ```

2. Check if your trained model exists and is being found by the application
3. Verify your data.yaml file has the correct class definitions
4. Lower the confidence threshold in model.py if needed

## Reference

- YOLOv8: https://github.com/ultralytics/ultralytics
- For more information, see [Ultralytics Documentation](https://docs.ultralytics.com/)
