""" Controller for a automation robot or that can be controlled via the gui."""
import threading
import time

class Robot:
    """Controller for the automation robot that can be controlled via the GUI."""
    def __init__(self, gui, model):
        self.gui = gui
        self.model = model
        self.is_running = False
        self.thread = None

    def start_robot(self):
        """Start the robot."""
        self.is_running = True
        self.gui.toggle_camera()
        self.gui.log_robot_action("Robot started")
        self.thread = threading.Thread(target=self.drive_loop, daemon=True)
        self.thread.start()

    def stop_robot(self):
        """Stop the robot."""
        self.is_running = False
        # only join the thread if it is alive and not the current thread
        if self.thread and self.thread.is_alive() and threading.current_thread() != self.thread:
            self.thread.join()
        self.gui.toggle_camera()
        self.gui.log_robot_action("Robot stopped")

    def drive_loop(self):
        """Main loop for driving the robot."""
        while self.is_running:
            # Simulate driving logic
            self.gui.log_robot_action("Robot is driving forward...")
            ret, frame = self.gui.cap.read()
            if not ret:
                self.gui.log_robot_action("Failed to read from camera")
                self.stop_robot()
                break

            # Simulate processing the frame
            processed_image, result, weed_coords = self.model.detect_weeds(frame)
            self.gui.display_image(processed_image)
            self.gui.update_results(result)

            if "weed" in result.lower() and weed_coords:
                self.gui.log_robot_action("Weed detected, wait for robot to eliminate weeds...")
                for x, y in weed_coords:
                    self.eliminate_weeds(x, y)
                break
            time.sleep(0.5)

    def eliminate_weeds(self, x_coord=None, y_coord=None):
        """Eliminate detected weeds."""
        if x_coord is not None and y_coord is not None:
            self.gui.log_robot_action(f"Roboter arm is moving to ({x_coord}, {y_coord})")
            time.sleep(1) # Simulate moving to the weed coordinates
            self.gui.log_robot_action("Eliminating weed...")
            time.sleep(1)
            self.gui.log_robot_action("Weed eliminated.")
        else:
            self.gui.log_robot_action("No weed coordinates provided, cannot eliminate weeds.")


