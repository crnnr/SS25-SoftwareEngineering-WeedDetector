""" Test for the main module of the Weed Detector application."""
import unittest
from unittest.mock import patch, MagicMock
from app.main import main

class TestMain(unittest.TestCase):
    """Test cases for the main module of the Weed Detector application."""

    @patch("app.main.WeedDetectorController")
    @patch("app.main.WeedDetectorGUI")
    @patch("app.main.WeedDetectorModel")
    def test_main_creates_and_runs_everything(self, mock_model, mock_gui, mock_controller):
        """Tests that the main function initializes the model, GUI, and controller correctly."""
        mock_model_instance = MagicMock()
        mock_gui_instance = MagicMock()
        mock_controller_instance = MagicMock()
        mock_model.return_value = mock_model_instance
        mock_gui.return_value = mock_gui_instance
        mock_controller.return_value = mock_controller_instance

        main()

        mock_model.assert_called_once()
        mock_gui.assert_called_once()
        mock_controller.assert_called_once_with(mock_model_instance, mock_gui_instance)
        mock_controller_instance.run.assert_called_once()

if __name__ == "__main__":
    unittest.main()
