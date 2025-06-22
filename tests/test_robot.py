""" Unit tests for the Robot class."""
import unittest
from unittest.mock import MagicMock, patch
from app.robot import Robot

class TestRobot(unittest.TestCase):
    """Test cases for the Robot class."""
    def setUp(self):
        """Set up the Robot instance with mocked GUI and model."""
        self.mock_gui = MagicMock()
        self.mock_model = MagicMock()
        self.robot = Robot(self.mock_gui, self.mock_model)

    def test_start_sets_running_and_logs_action(self):
        """Tests the start method sets running to True and logs the action."""
        self.robot.is_running = False
        self.robot.start_robot()
        self.assertTrue(self.robot.is_running)
        self.mock_gui.log_robot_action.assert_any_call("Robot started")
        self.mock_gui.toggle_camera.assert_called_once()

    def test_stop_sets_running_false_and_logs_action(self):
        """Tests the stop method sets running to False and logs the action."""
        self.robot.is_running = True
        self.robot.stop_robot()
        self.assertFalse(self.robot.is_running)
        self.mock_gui.log_robot_action.assert_any_call("Robot stopped")

    @patch("time.sleep", return_value=None)
    def test_drive_loop_stops_on_weed(self, _):
        """Tests the drive_loop method stops when a weed is detected."""
        self.robot.is_running = True
        self.mock_gui.cap.read.side_effect = [
            (True, "frame1"),
            (True, "frame2"),
        ]
        # first picture has no weed, second has weed
        self.mock_model.detect_weeds.side_effect = [
            ("processed1", "No weeds detected"),
            ("processed2", "Weed detected!"),
        ]
        # drive_loop should stop after detecting a weed
        self.robot.drive_loop()
        self.mock_gui.display_image.assert_any_call("processed1")
        self.mock_gui.display_image.assert_any_call("processed2")
        self.mock_gui.update_results.assert_any_call("No weeds detected")
        self.mock_gui.update_results.assert_any_call("Weed detected!")
        self.mock_gui.log_robot_action.assert_any_call("Weed detected! Robot stopped.")
        self.assertFalse(self.robot.running)

    @patch("time.sleep", return_value=None)
    def test_drive_loop_stops_on_camera_error(self, _):
        """Tests the drive_loop method stops if camera read fails."""
        self.robot.is_running = True
        self.mock_gui.cap.read.return_value = (False, None)
        self.robot.drive_loop()
        self.mock_gui.log_robot_action.assert_any_call("Camera error. Robot stopped.")
        self.assertFalse(self.robot.running)

if __name__ == "__main__":
    unittest.main()