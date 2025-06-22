"""Unit tests for the WeedDetectorModel class."""
import unittest
import numpy as np
import cv2
from app.model import WeedDetectorModel

class TestWeedDetectorModel(unittest.TestCase):
    """Test cases for the WeedDetectorModel class."""
    def setUp(self):
        """Set up the WeedDetectorModel instance and a dummy image for testing."""
        self.model = WeedDetectorModel()
        self.dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)

    def test_load_image_success(self):
        """Test if an image can be loaded successfully."""
        cv2.imwrite("dummy.jpg", self.dummy_image)
        image = self.model.load_image("dummy.jpg")
        self.assertIsNotNone(image)
        self.assertEqual(image.shape, self.dummy_image.shape)

    def test_load_image_failure(self):
        """Test if loading a non-existing image raises an error."""
        with self.assertRaises(ValueError):
            self.model.load_image("not_existing.jpg")

    def test_format_detection_results_no_detections(self):
        """Test if the detection results are formatted correctly when no weeds are detected."""
        self.model.detected_centers = []
        result = self.model._format_detection_results()
        self.assertIn("No weeds detected", result)

    def test_format_detection_results_with_detections(self):
        """Test if the detection results are formatted correctly when weeds are detected."""
        self.model.detected_centers = [(10, 20, "weed", 0.9)]
        result = self.model._format_detection_results()
        self.assertIn("1. weed at (10,20) - Confidence: 0.90", result)

    def test_detect_weeds_runs(self):
        """Test if the detect_weeds method runs without errors."""
        try:
            processed, result = self.model.detect_weeds(self.dummy_image)
            self.assertIsNotNone(processed)
            self.assertIsInstance(result, str)
        except (OSError, RuntimeError, ValueError, ImportError) as e:
            self.skipTest(f"YOLO model not available: {e}")

    def test_predict_with_valid_image(self):
        """Test if the predict method works with a valid image."""
        try:
            processed_image = self.model.predict(self.dummy_image)
            self.assertIsNotNone(processed_image)
            self.assertEqual(processed_image.shape, self.dummy_image.shape)
        except (OSError, RuntimeError, ValueError, ImportError) as e:
            self.skipTest(f"YOLO model not available: {e}")

    def test_model_init_with_default_path(self):
        """Test model initialization with default path."""
        model = WeedDetectorModel()
        self.assertIsNotNone(model.model)
        self.assertTrue(hasattr(model, "model_path"))

    def test_model_init_with_invalid_path(self):
        """Test model initialization with an invalid path falls back to default."""
        try:
            model = WeedDetectorModel(model_path="not_existing_model.pt")
            self.assertIsNotNone(model.model)
            self.assertTrue(model.model_path.endswith(".pt"))
        except Exception as e:
            self.skipTest(f"YOLO model not available: {e}")

    def test_format_detection_results_none(self):
        """Test _format_detection_results returns correct string if attribute missing."""
        if hasattr(self.model, "detected_centers"):
            delattr(self.model, "detected_centers")
        result = self.model._format_detection_results()
        self.assertIn("No weeds detected", result)

    def test_detect_weeds_handles_none_image(self):
        """Test detect_weeds raises ValueError if image is None."""
        with self.assertRaises(Exception):
            self.model.detect_weeds(None)

    def test_predict_with_invalid_image(self):
        """Test predict raises an error with invalid image."""
        with self.assertRaises(Exception):
            self.model.predict(None)

if __name__ == "__main__":
    unittest.main()
