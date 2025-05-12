"""Weed Detector Model using YOLOv8"""
import cv2
import numpy as np
from ultralytics import YOLO

class WeedDetectorModel:
    def __init__(self, model_path):
        """Initialize the Weed Detector Model."""
        self.model = YOLO(model_path)
        if self.model is None:
            raise ValueError("Model not found or invalid model path.")
        self.model.fuse()  # Fuse model layers for faster inference
        self.model.conf = 0.25  # Set confidence threshold
        self.model.iou = 0.45  # Set IoU threshold for NMS
        self.model.classes = [0]  # Only detect class 0 (weed)
    
    def predict(self, image_path):
        """Perform detection on the input image."""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or invalid image path.")
        
        results = self.model.predict(source=image, conf=0.25)
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                score = box.conf[0]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                name = self.model.names[cls_id]
                
                # Draw bounding box and label
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(image, (cx, cy), 5, (0, 0, 255), -1)
                cv2.putText(image, f"{name} {score:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return image
    
    def train(self, train_data_path, epochs=50):
        """Train the model on the provided dataset."""
        self.model.train(data=train_data_path, epochs=epochs)

    def evaluate(self, val_data_path):
        """Evaluate the model on the validation dataset."""
        results = self.model.val(data=val_data_path)
        return results
    
    def save_model(self, save_path):
        """Save the trained model to the specified path."""
        self.model.save(save_path)