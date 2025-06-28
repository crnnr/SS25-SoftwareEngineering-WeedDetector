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
    def test_drive_loop_runs_until_weeds(self, _):
        """Tests the drive_loop method runs until weeds are detected."""
        self.robot.is_running = True
        self.mock_gui.cap.read.return_value = (True, "frame")
        self.mock_model.detect_weeds.return_value = ("processed_image", "weed detected")

        self.robot.drive_loop()
        self.mock_gui.log_robot_action.assert_any_call("Robot is driving forward...")
        self.mock_model.detect_weeds.assert_called_once_with("frame")
        self.mock_gui.display_image.assert_called_with("processed_image")
        self.mock_gui.update_results.assert_called_with("weed detected")
        self.mock_gui.log_robot_action.assert_any_call("Weed detected, stopping robot.")
        self.assertFalse(self.robot.is_running)

    @patch("time.sleep", return_value=None)
    def test_drive_loop_stops_on_camera_error(self, _):
        """Tests the drive_loop method stops if camera read fails."""
        self.robot.is_running = True
        self.mock_gui.cap.read.return_value = (False, None)
        self.robot.drive_loop()
        self.mock_gui.log_robot_action.assert_any_call("Failed to read from camera")
        self.assertFalse(self.robot.is_running)
    
    @patch("time.sleep", return_value=None)
    def test_eliminate_weeds_logs_actions(self, _):
        """Tests the eliminate_weeds method logs the correct actions."""
        x_coord, y_coord = 100, 200
        self.robot.eliminate_weeds(x_coord, y_coord)
        self.mock_gui.log_robot_action.assert_any_call(f"Roboter arm is moving to ({x_coord}, {y_coord})")
        self.mock_gui.log_robot_action.assert_any_call("Eliminating weed...")
        self.mock_gui.log_robot_action.assert_any_call("Weed eliminated.")

if __name__ == "__main__":
    unittest.main()
