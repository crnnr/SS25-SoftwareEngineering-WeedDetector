"""System test for the Weed Detector application. This test simulates the full detection flow."""
import unittest
import os
import cv2
from app.model import WeedDetectorModel
from app.gui import WeedDetectorGUI
from app.controller import WeedDetectorController

class TestSystem(unittest.TestCase):
    """System test for the Weed Detector application."""

    def setUp(self):
        self.model = WeedDetectorModel()
        self.gui = WeedDetectorGUI()
        self.controller = WeedDetectorController(self.model, self.gui)
        # Use a real image from the workspace
        self.image_path = os.path.abspath("unkraut1.jpg")
        self.assertTrue(os.path.exists(self.image_path), "Test image not found.")

    def test_full_detection_flow(self):
        """Simulate user uploading an image and verify detection and GUI update."""
        # Simulate user selects image
        image = self.model.load_image(self.image_path)
        processed, result = self.model.detect_weeds(image)
        # Display in GUI
        self.gui.display_image(processed)
        self.gui.update_results(result)
        # Check that results are shown in the GUI
        gui_content = self.gui.results_text.get("1.0", "end")
        self.assertIn("weed", gui_content.lower())
        self.assertGreater(len(gui_content.strip()), 0)

if __name__ == "__main__":
    unittest.main()
