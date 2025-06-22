""" Unit tests for the GUI module. """
import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from app.gui import WeedDetectorGUI

class TestWeedDetectorGUI(unittest.TestCase):
    """Unit tests for the WeedDetectorGUI class."""

    def setUp(self):
        """Set up the GUI for testing."""
        self.root = tk.Tk()
        self.gui = WeedDetectorGUI(MagicMock())
        self.gui.master = self.root

    def tearDown(self):
        """Destroy the GUI after tests."""
        self.root.destroy()

    def test_initialization(self):
        """Test if the GUI initializes correctly."""
        self.assertIsInstance(self.gui, WeedDetectorGUI) # See if gui is instance of WeedDetectorGUI
        self.assertTrue(hasattr(self.gui, 'select_image_button'))
        self.assertTrue(hasattr(self.gui, 'detect_button'))

    @patch('tkinter.filedialog.askopenfilename')
    def test_select_image(self, mock_askopenfilename):
        """Test the select image functionality."""
        mock_askopenfilename.return_value = 'test_image.jpg'
        self.gui.select_btn.invoke() # Simulate button click
        mock_askopenfilename.assert_called_once()

    def test_display_image(self):
        """Test if the display image method works."""
        # Assuming display_image method updates a label with an image
        image = tk.PhotoImage()  # Mock image
        self.gui.display_image(image)
        # Check if the label has been updated with the image
        self.assertEqual(self.gui.image_label.image, image)

    def test_update_results(self):
        """Test if results are updated correctly."""
        result = "Detected weeds: 5"
        self.gui.update_results(result)
        # Check if the result label has been updated
        self.assertEqual(self.gui.result_label['text'], result)

    @patch('tkinter.messagebox.showerror')
    def test_show_error_box(self, mock_showerror):
        """Test if error box is shown correctly."""
        self.gui.show_error_box("Fehlertext")
        mock_showerror.assert_called_with("Error", "Fehlertext")
        content = self.gui.results_text.get("1.0", tk.END)
        self.assertIn("Error: Fehlertext", content)

    def test_update_live_results(self):
        """Test if live results are updated correctly."""
        self.gui.camera_running = True
        self.gui.results_text.config(state=tk.NORMAL)
        self.gui.results_text.delete("1.0", tk.END)
        self.gui.results_text.insert(tk.END, "Camera started\n")
        self.gui.results_text.config(state=tk.DISABLED)
        self.gui.update_live_results("Live detection!")
        content = self.gui.results_text.get("1.0", tk.END)
        self.assertIn("Live detection!", content)

    def test_toggle_camera_start_and_stop(self):
        """Test toggling the camera on and off."""
        # Starte Kamera (mock cv2.VideoCapture)
        with patch('cv2.VideoCapture') as mock_cap:
            mock_instance = MagicMock()
            mock_instance.isOpened.return_value = True
            mock_cap.return_value = mock_instance
            self.gui.toggle_camera()
            self.assertTrue(self.gui.camera_running)
            self.assertEqual(self.gui.camera_btn['text'], "⏹ Stop Camera")
            self.gui.toggle_camera()
            self.assertFalse(self.gui.camera_running)
            self.assertEqual(self.gui.camera_btn['text'], "📷 Start Camera")

if __name__ == "__main__":
    unittest.main()
