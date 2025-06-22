"""Unit tests for the WeedDetectorController class."""

import unittest
from unittest.mock import MagicMock
from app.controller import WeedDetectorController

class TestWeedDetectorController(unittest.TestCase):
    """Test cases for the WeedDetectorController class."""
    def setUp(self):
        self.mock_model = MagicMock() # Mock WeedDetectorModel
        self.mock_gui = MagicMock() # Mock WeedDetectorGUI
        self.mock_gui.conf_var.get.return_value = 0.15
        self.controller = WeedDetectorController(self.mock_model, self.mock_gui)

    def test_handle_select_image_success(self):
        """Tests the handle_select_image method for successful image loading."""
        # model.load_image retunts a dummy image
        dummy_image = "image"
        self.mock_model.load_image.return_value = dummy_image

        # handle_select_image sollte display_image aufrufen
        self.controller.handle_select_image("test.jpg")
        self.mock_model.load_image.assert_called_with("test.jpg")
        self.mock_gui.display_image.assert_called_with(dummy_image)

    def test_handle_select_image_failure(self):
        """Tests the handle_select_image method for failure cases."""
        self.mock_model.load_image.side_effect = ValueError("Fehler beim Laden des Bildes: test")
        self.controller.handle_select_image("fail.jpg")
        args, kwargs = self.mock_gui.show_error_box.call_args # Get the arguments passed to show_error_box
        self.assertTrue(args[0].startswith("Fehler beim Laden des Bildes:"))

    def test_handle_detect_success(self):
        """Tests the handle_detect method for successful detection with a real image."""
        # use a real image for testing
        image_path = "unkraut1.jpg"
        # model is loading the real image
        self.mock_model.load_image.return_value = image_path
        dummy_processed = "processed"
        dummy_result = "result"
        self.mock_model.detect_weeds.return_value = (dummy_processed, dummy_result)
        self.controller.handle_detect(image_path)
        self.mock_model.load_image.assert_called_with(image_path)
        self.mock_model.detect_weeds.assert_called_with(image_path)
        self.mock_gui.display_image.assert_called_with(dummy_processed)
        self.mock_gui.update_results.assert_called_with(f"Detection with confidence 0.15: {dummy_result}")

    def test_handle_detect_failure(self):
        """Tests the handle_detect method for failure cases."""
        self.mock_model.load_image.side_effect = ValueError("Fehler")
        self.controller.handle_detect("fail.jpg")
        self.mock_gui.show_error_box.assert_called()

    def test_handle_start_robot(self):
        """Tests the handle_start_robot method."""
        self.controller.handle_start_robot()
        self.mock_gui.toggle_camera.assert_called_once()
        self.mock_gui.log_robot_action.assert_called_with("Robot is driving forward...")

    def test_handle_stop_robot(self):
        """Tests the handle_stop_robot method."""
        self.controller.handle_stop_robot()
        self.mock_gui.toggle_camera.assert_called_once()
        self.mock_gui.log_robot_action.assert_called_with("Robot stopped")

    def test_handle_camera_frame(self):
        """Tests the handle_camera_frame method."""
        dummy_frame = "frame"
        confidence = 0.15
        self.mock_model.predict.return_value = ("processed_frame")
        processed_frame, centers = self.controller.handle_camera_frame(dummy_frame, confidence)
        self.mock_model.predict.assert_called_with(dummy_frame)
        self.assertEqual(processed_frame, "processed_frame")
        self.assertEqual(centers, [])

    def test_handle_camera_frame_exception(self):
        """Tests handle_camera_frame when model.predict raises an exception."""
        dummy_frame = "frame"
        confidence = 0.15
        self.mock_model.predict.side_effect = RuntimeError("Prediction failed")
        with self.assertRaises(RuntimeError):
            self.controller.handle_camera_frame(dummy_frame, confidence)

if __name__ == "__main__":
    unittest.main()
