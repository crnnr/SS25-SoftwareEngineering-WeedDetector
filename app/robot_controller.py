""" Controller for a automation robot or that can be controled via the gui."""

class RobotController:
    def __init__(self):
        """Initializes the RobotController."""
        self.active = False

    def start(self):
        """Starts the robot."""
        if not self.active:
            self.active = True
            print("Robot started.")
        else:
            print("Robot is already running.")
    
    def stop(self):
        """Stops the robot."""
        if self.active:
            self.active = False
            print("Robot stopped.")
        else:
            print("Robot is not running.")

    def move_forward(self, distance):
        """Moves the robot forward by a specified distance."""
        if self.active:
            print(f"Moving forward {distance} units.")
        else:
            print("Robot is not running. Cannot move.")

    def stop_moving(self):
        """Stops the robot's movement."""
        if self.active:
            print("Stopping movement.")
        else:
            print("Robot is not running. Cannot stop moving.")