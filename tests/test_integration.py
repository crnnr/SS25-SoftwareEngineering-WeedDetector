import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import os
import cv2
from app.model import WeedDetectorModel
from app.gui import WeedDetectorGUI
from app.controller import WeedDetectorController

class TestIntegration(unittest.TestCase):
    """Integration tests for the Weed Detector application."""
    def setUp(self):
        self.model = WeedDetectorModel()
        self.dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)

    def test_controller_detect_flow(self):
        """Test: controller detects weeds using model and updates GUI."""
        gui = MagicMock()
        controller = WeedDetectorController(self.model, gui)
        with patch.object(self.model, "load_image", return_value=self.dummy_image):
            with patch.object(self.model, "detect_weeds",
                               return_value=("processed", "result")) as mock_detect:
                controller.handle_detect("dummy.jpg")
                mock_detect.assert_called_with(self.dummy_image)
                gui.display_image.assert_called_with("processed")
                gui.update_results.assert_called()

    def test_gui_and_model_integration(self):
        """Test: gui displays an image loaded by the model."""
        gui = WeedDetectorGUI()
        image = self.model.load_image("dummy.jpg") \
            if hasattr(self.model, "load_image") else self.dummy_image
        gui.display_image(image)
        gui.root.update()
        items = gui.canvas.find_all()
        self.assertGreater(len(items), 0)

    def test_model_detect_weeds_with_real_image(self):
        """Test: mnodel detects weeds and returns results."""
        image_path = os.path.join(os.path.dirname(__file__), "..", "unkraut1.jpg")
        image_path = os.path.abspath(image_path)
        if not os.path.exists(image_path):
            self.skipTest("unkraut1.jpg not found")
        image = cv2.imread(image_path)
        processed, result = self.model.detect_weeds(image)
        self.assertIsNotNone(processed)
        self.assertIsInstance(result, str)

    def test_controller_handles_load_image_failure(self):
        """Test: controller shows error if image loading fails."""
        gui = MagicMock()
        controller = WeedDetectorController(self.model, gui)
        with patch.object(self.model, "load_image", side_effect=ValueError("Fehler beim Laden")):
            controller.handle_select_image("notfound.jpg")
            gui.show_error_box.assert_called()
            self.assertIn("Fehler", gui.show_error_box.call_args[0][0])

    def test_controller_handles_detect_failure(self):
        """Test: controller shows error if weed detection fails."""
        gui = MagicMock()
        controller = WeedDetectorController(self.model, gui)
        with patch.object(self.model, "load_image", return_value=self.dummy_image):
            with patch.object(self.model, "detect_weeds",
                               side_effect=ValueError("Detection failed")):
                controller.handle_detect("dummy.jpg")
                gui.show_error_box.assert_called()
                self.assertIn("Detection failed", gui.show_error_box.call_args[0][0])

    def test_controller_robot_start_and_stop(self):
        """Test: controller starts and stops the robot correctly."""
        gui = MagicMock()
        controller = WeedDetectorController(self.model, gui)
        controller.handle_start_robot()
        gui.toggle_camera.assert_called_once()
        gui.log_robot_action.assert_called_with("Robot is driving forward...")
        controller.handle_stop_robot()
        gui.log_robot_action.assert_called_with("Robot stopped")

    def test_gui_select_image_cancel(self):
        """Test:gui handles image selection cancel."""
        gui = WeedDetectorGUI()
        with patch("tkinter.filedialog.askopenfilename", return_value=""):
            gui.select_image()

    def test_gui_display_image_with_invalid_input(self):
        """Test:gui shows error when displaying invalid image."""
        gui = WeedDetectorGUI()
        with patch.object(gui, "show_error_box") as mock_error:
            gui.display_image(None)
            mock_error.assert_called()

if __name__ == "__main__":
    unittest.main()