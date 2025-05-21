import cv2
import os
from ultralytics import YOLO
import numpy as np

class WeedDetectorModel:
    def __init__(self, model_path="yolov8n.pt"):
        self.model_path = model_path
        possible_trained_models = [
            "runs/detect_train/weights/best.pt",
            "data/weights/best.pt",
            "data/models/best.pt",
            "models/best.pt",
        ]
        
        trained_model_found = False
        for trained_path in possible_trained_models:
            if os.path.exists(trained_path):
                self.model_path = trained_path
                print(f"Found trained weed detection model at {trained_path}")
                trained_model_found = True
                break
                
        if not trained_model_found:
            print(f"No trained weed detection model found, using default model: {model_path}")
        
        try:
            self.model = YOLO(self.model_path)
            print(f"Model class names: {self.model.names}")
        except Exception as e:
            print(f"Error loading model {self.model_path}: {e}")
            print(f"Falling back to default model {model_path}")
            self.model_path = model_path
            self.model = YOLO(model_path)
            print(f"Default model class names: {self.model.names}")
            
        if self.model is None:
            raise ValueError("Model not found or invalid model path.")
        self.model.fuse()
        self.model.conf = 0.15
        self.model.iou = 0.45
        print(f"Loaded detection model: {self.model_path}")

    def predict(self, image):
        image_source = image
        is_path = isinstance(image, str)
        
        if is_path:
            print(f"Loading image from path: {image}")
            image = cv2.imread(image)
            if image is None:
                raise ValueError(f"Image not found or invalid image path: {image_source}")
        
        processed_image = image.copy()
        
        print(f"Image shape: {processed_image.shape}")
        
        try:
            results = self.model.predict(image, conf=0.05, verbose=False)
            
            print(f"Detection results: {len(results)} items")
            detections_found = False
            
            for i, r in enumerate(results):
                print(f"Result {i}: has boxes: {hasattr(r, 'boxes')}")
                if hasattr(r, 'boxes') and r.boxes is not None:
                    num_boxes = len(r.boxes)
                    print(f"Number of boxes detected: {num_boxes}")
                    
                    if num_boxes > 0:
                        detections_found = True
                        
                    for box in r.boxes:
                        b = box.xyxy[0].cpu().numpy().astype(int)
                        c = int(box.cls[0])
                        conf = float(box.conf[0])
                        class_name = self.model.names[c]
                        
                        print(f"Box: {b}, Class: {class_name}, Confidence: {conf:.2f}")
                        
                        b[0] = max(0, b[0])
                        b[1] = max(0, b[1])
                        b[2] = min(processed_image.shape[1] - 1, b[2])
                        b[3] = min(processed_image.shape[0] - 1, b[3])
                        
                        cv2.rectangle(processed_image, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 2)
                        
                        label = f"{class_name} {conf:.2f}"
                        cv2.putText(
                            processed_image,
                            label,
                            (b[0], max(b[1] - 10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 0, 255),
                            2
                        )
            
            if not detections_found:
                print("No detections found in this image")
                text = "No objects detected"
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
                text_x = (processed_image.shape[1] - text_size[0]) // 2
                text_y = (processed_image.shape[0] + text_size[1]) // 2
                cv2.putText(
                    processed_image,
                    text,
                    (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 0, 255),
                    2
                )
                
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            import traceback
            traceback.print_exc()
            return image  # Return original image on error
            
        return processed_image

    def train(self, train_data_path, epochs=50):
        self.model.train(data=train_data_path, epochs=epochs)

    def evaluate(self, val_data_path):
        results = self.model.val(data=val_data_path)
        return results

    def save_model(self, save_path):
        self.model.save(save_path)