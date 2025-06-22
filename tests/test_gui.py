""" Unit tests for the GUI module. """
import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from app.gui import WeedDetectorGUI

class TestWeedDetectorGUI(unittest.TestCase):
    """Unit tests for the WeedDetectorGUI class."""

    @classmethod
    def setUpClass(cls):
        """Set up the GUI for testing."""
        cls.root = tk.Tk()
        cls.root.withdraw()  # Hide the root window for testing

    @classmethod
    def tearDownClass(cls):
        """Destroy the GUI after tests."""
        cls.root.destroy()

    def setUp(self):
        """Set up the GUI for testing."""
        self.gui = WeedDetectorGUI()
        self.gui.master = self.root

    def tearDown(self):
        """Destroy the GUI after tests."""
        self.gui.canvas.destroy()
        self.gui = None

    def test_initialization(self):
        """Test if the GUI initializes correctly."""
        self.assertIsInstance(self.gui, WeedDetectorGUI) # See if gui is instance of WeedDetectorGUI
        self.assertTrue(hasattr(self.gui, 'select_btn'))
        self.assertTrue(hasattr(self.gui, 'camera_btn'))
        self.assertTrue(hasattr(self.gui, 'robot_btn'))

    @patch('tkinter.filedialog.askopenfilename')
    def test_select_image(self, mock_askopenfilename):
        """Test the select image functionality."""
        mock_askopenfilename.return_value = 'test_image.jpg'
        self.gui.select_btn.invoke() # Simulate button click
        mock_askopenfilename.assert_called_once()

    def test_display_image(self):
        """Test if display_image draws an image on the canvas."""
        import cv2
        import os

        image_path = os.path.join(os.path.dirname(__file__), "..", "unkraut1.jpg")
        image_path = os.path.abspath(image_path)
        self.assertTrue(os.path.exists(image_path), "Image file does not exist.")

        cv_image = cv2.imread(image_path)
        self.assertIsNotNone(cv_image, "Failed to read the image file.")

        self.gui.canvas.config(width=400, height=300)
        self.gui.canvas.update()
        self.gui.display_image(cv_image)
        self.root.update()
        items = self.gui.canvas.find_all()
        self.assertGreater(len(items), 0)

    def test_update_results(self):
        """Test if results are updated correctly."""
        result = "Detected weeds: 5"
        self.gui.update_results(result)
        content = self.gui.results_text.get("1.0", tk.END)
        self.assertIn(result, content)

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

    def test_start_robot(self):
        """Test starting the robot."""
        with patch('app.robot.Robot.start_robot'):
            self.gui.robot_btn.invoke()

    def test_stop_robot(self):
        """Test stopping the robot."""
        with patch('app.robot.Robot.stop_robot'):
            self.gui.robot_btn.invoke()

    def test_log_robot_action(self):
        """Test logging robot actions."""
        self.gui.log_robot_action("Robot started")
        content = self.gui.robot_actions_text.get("1.0", tk.END)
        self.assertIn("Robot started", content)

        self.gui.log_robot_action("Robot stopped")
        content = self.gui.robot_actions_text.get("1.0", tk.END)
        self.assertIn("Robot stopped", content)

if __name__ == "__main__":
    unittest.main()
