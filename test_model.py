#!/usr/bin/env python
# Test script to verify model detection capabilities

import cv2
import os
import sys
from ultralytics import YOLO
from pathlib import Path

def test_model(model_path, image_path, conf_threshold=0.05):
    """Test a YOLO model on an image and display the results"""
    print(f"Testing model: {model_path}")
    print(f"Image path: {image_path}")
    
    # Verify files exist
    if not os.path.exists(model_path):
        print(f"ERROR: Model file not found at {model_path}")
        return False
        
    if not os.path.exists(image_path):
        print(f"ERROR: Image file not found at {image_path}")
        return False
    
    # Load model
    try:
        model = YOLO(model_path)
        print(f"Model loaded. Class names: {model.names}")
    except Exception as e:
        print(f"ERROR loading model: {e}")
        return False
    
    # Load image
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"ERROR: Failed to read image at {image_path}")
            return False
        print(f"Image loaded. Shape: {image.shape}")
    except Exception as e:
        print(f"ERROR loading image: {e}")
        return False
    
    # Run detection
    try:
        # Set a very low confidence threshold to ensure we get some detections
        results = model.predict(image, conf=conf_threshold, verbose=True)
        
        # Process results
        detections_found = False
        for i, r in enumerate(results):
            if hasattr(r, 'boxes') and r.boxes is not None:
                num_boxes = len(r.boxes)
                print(f"Number of objects detected: {num_boxes}")
                
                if num_boxes > 0:
                    detections_found = True
                    for box in r.boxes:
                        b = box.xyxy[0].cpu().numpy().astype(int)
                        c = int(box.cls[0])
                        conf = float(box.conf[0])
                        class_name = model.names[c]
                        
                        print(f"  - {class_name}: confidence={conf:.2f}, box={b}")
                        
                        # Draw rectangle
                        cv2.rectangle(image, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 2)
                        
                        # Draw label
                        label = f"{class_name} {conf:.2f}"
                        cv2.putText(image, label, (b[0], b[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                                  0.5, (0, 0, 255), 2)
        
        if not detections_found:
            print("No objects detected in this image.")
            # Add text to image
            cv2.putText(image, "No objects detected", (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Save the result
        output_path = "detection_result.jpg"
        cv2.imwrite(output_path, image)
        print(f"Result saved to {output_path}")
        
        # Try to display the image (will work in environments with display)
        try:
            cv2.imshow("Detection Result", image)
            print("Press any key to close the image window...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except:
            print("Could not display image (probably running in headless environment)")
        
        return detections_found
            
    except Exception as e:
        print(f"ERROR during detection: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run tests with different models and thresholds"""
    # Check command line arguments
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Try to find a sample image
        sample_images = ["sample.jpg", "test.jpg", "image.jpg"]
        image_path = None
        for img in sample_images:
            if os.path.exists(img):
                image_path = img
                break
        
        if image_path is None:
            print("ERROR: No image specified. Please provide an image path as argument.")
            print("Usage: python test_model.py path/to/image.jpg")
            return
    
    # Find models to test
    models_to_test = []
    
    # Check for custom trained model first
    custom_models = [
        "runs/detect_train/weights/best.pt", 
        "models/best.pt",
        "data/models/best.pt"
    ]
    
    for model_path in custom_models:
        if os.path.exists(model_path):
            models_to_test.append((model_path, 0.25, "Custom trained model"))
            break
    
    # Always test with default model
    models_to_test.append(("yolov8n.pt", 0.05, "Default YOLOv8n model"))
    
    # Run tests
    for model_path, threshold, description in models_to_test:
        print(f"\n\n===== Testing {description} =====")
        found = test_model(model_path, image_path, threshold)
        print(f"Detection {'successful' if found else 'failed'}")

if __name__ == "__main__":
    main()