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
        # Dummy-Bild (100x100, 3 Kanäle)
        self.dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)

    def test_load_image_success(self):
        """Test if an image can be loaded successfully."""
        # Schreibe ein Dummy-Bild auf die Platte
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
        # Da YOLO-Modell geladen wird, kann dieser Test fehlschlagen,
        # wenn das Modell nicht vorhanden ist.
        # Wir testen nur, ob die Methode ohne Exception läuft.
        try:
            processed, result = self.model.detect_weeds(self.dummy_image)
            self.assertIsNotNone(processed)
            self.assertIsInstance(result, str)
        except (OSError, RuntimeError, ValueError, ImportError) as e:
            self.skipTest(f"YOLO model not available: {e}")

if __name__ == "__main__":
    unittest.main()
