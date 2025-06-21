"""Unit tests for the WeedDetectorController class."""

import unittest
from unittest.mock import MagicMock
from controller import WeedDetectorController

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
        # Model.load_image wirft Exception
        self.mock_model.load_image.side_effect = Exception("Fehler")
        self.controller.handle_select_image("fail.jpg")
        self.mock_gui.show_error_box.assert_called()

    def test_handle_detect_success(self):
        """Tests the handle_detect method for successful detection."""
        dummy_image = "image" # Mock image
        dummy_processed = "processed" # Mock processed image
        dummy_result = "result" # Mock detection result
        self.mock_model.load_image.return_value = dummy_image
        self.mock_model.detect_weeds.return_value = (dummy_processed, dummy_result)
        # handle_detect should call load_image, detect_weeds, display_image, and update_results
        self.controller.handle_detect("test.jpg")
        self.mock_model.load_image.assert_called_with("test.jpg")
        self.mock_model.detect_weeds.assert_called_with(dummy_image)
        self.mock_gui.display_image.assert_called_with(dummy_processed)
        self.mock_gui.update_results.assert_called_with(dummy_result)

    def test_handle_detect_failure(self):
        """Tests the handle_detect method for failure cases."""
        self.mock_model.load_image.side_effect = Exception("Fehler")
        self.controller.handle_detect("fail.jpg")
        self.mock_gui.show_error_box.assert_called()

if __name__ == "__main__":
    unittest.main()
