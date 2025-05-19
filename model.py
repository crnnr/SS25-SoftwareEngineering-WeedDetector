import cv2
from ultralytics import YOLO

class WeedDetectorModel:
    def __init__(self, model_path="yolo11n.pt"):
        self.model_path = model_path
        self.model = YOLO(model_path)
        if self.model is None:
            raise ValueError("Model not found or invalid model path.")
        self.model.fuse()
        self.model.conf = 0.25
        self.model.iou = 0.45
        print(f"Loaded detection model: {model_path}")

    def predict(self, image):
        if isinstance(image, str):
            image = cv2.imread(image)
            if image is None:
                raise ValueError("Image not found or invalid image path.")
        results = self.model.predict(source=image, conf=0.25, verbose=False)
        for r in results:
            if hasattr(r, 'boxes') and r.boxes is not None:
                for box in r.boxes:
                    b = box.xyxy[0].cpu().numpy().astype(int)
                    c = int(box.cls[0])
                    conf = float(box.conf[0])
                    class_name = self.model.names[c]
                    cv2.rectangle(image, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 2)
                    label = f"{class_name} {conf:.2f}"
                    cv2.putText(
                        image,
                        label,
                        (b[0], b[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 0, 255),
                        2
                    )
        return image

    def train(self, train_data_path, epochs=50):
        self.model.train(data=train_data_path, epochs=epochs)

    def evaluate(self, val_data_path):
        results = self.model.val(data=val_data_path)
        return results

    def save_model(self, save_path):
        self.model.save(save_path)