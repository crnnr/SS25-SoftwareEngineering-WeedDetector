""" Controller for a automation robot or that can be controled via the gui."""
import threading
import time

class Robot:
    def __init__(self, gui, model):
        self.gui = gui
        self.model = model
        self.is_running = False
        self.thread = None

        # Set up GUI callbacks
        self.gui.on_start_robot = self.start_robot
        self.gui.on_stop_robot = self.stop_robot
    
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
        if self.thread and self.thread.is_alive():
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
            processed_image, result = self.model.detect_weeds(frame)
            self.gui.display_image(processed_image)
            self.gui.update_results(result)

            if "weed" in result.lower():
                self.gui.log_robot_action("Weed detected, stopping robot.")
                self.stop_robot()
                break
            time.sleep(0.5)