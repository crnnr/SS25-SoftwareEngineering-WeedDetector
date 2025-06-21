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

    def load_image(self, image_path):
        """Loads an image from the given path."""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Image not found or invalid image path: {image_path}")
        return image

    def detect_weeds(self, image):
        """Detects weeds in the given image using the YOLO model."""
        processed_image = self.predict(image)
        result_text = self._format_detection_results()
        return processed_image, result_text

    def _format_detection_results(self):
        """Formats the detection results into a readable string."""
        if not hasattr(self, 'detected_centers') or not self.detected_centers:
            return "No weeds detected"

        lines = []
        for i, (x, y, class_name, conf) in enumerate(self.detected_centers, 1):
            lines.append(f"{i}. {class_name} at ({x},{y}) - Confidence: {conf:.2f}")
        return "\n".join(lines)

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
        print(f"Using confidence threshold: {self.model.conf}")

        try:
            # Use the model's current confidence setting
            results = self.model.predict(image, conf=self.model.conf, verbose=False)

            print(f"Detection results: {len(results)} items")
            detections_found = False

            # Reset detected centers for new prediction
            self.detected_centers = []

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

                        b[0] = max(0, b[0])
                        b[1] = max(0, b[1])
                        b[2] = min(processed_image.shape[1] - 1, b[2])
                        b[3] = min(processed_image.shape[0] - 1, b[3])

                        center_x = int((b[0] + b[2]) / 2)
                        center_y = int((b[1] + b[3]) / 2)

                        self.detected_centers.append((center_x, center_y, class_name, conf))

                        print(f"Box: {b}, Center: ({center_x}, {center_y}), "
                              f"Class: {class_name}, Confidence: {conf:.2f}")

                        cv2.rectangle(processed_image, (b[0], b[1]), (b[2], b[3]),
                                      (0, 0, 255), 2)

                        cross_size = 5
                        cv2.line(processed_image,
                               (center_x - cross_size, center_y),
                               (center_x + cross_size, center_y),
                               (0, 0, 255), 2)
                        cv2.line(processed_image,
                               (center_x, center_y - cross_size),
                               (center_x, center_y + cross_size),
                               (0, 0, 255), 2)

                        label = f"{class_name} ({center_x},{center_y}) {conf:.2f}"
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
                text = f"No objects detected (conf>{self.model.conf:.2f})"
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
            return image

        return processed_image

    def train(self, train_data_path, epochs=50):
        self.model.train(data=train_data_path, epochs=epochs)

    def evaluate(self, val_data_path):
        results = self.model.val(data=val_data_path)
        return results

    def save_model(self, save_path):
        self.model.save(save_path)