"""Controller module for the Weed Detector application.

This module contains the WeedDetectorController class that coordinates
interactions between the model, GUI, and robot components.
"""

import os
from model import WeedDetectorModel
from gui import WeedDetectorGUI
from robot import Robot


class WeedDetectorController:
    """Controller class that manages interactions between model, GUI, and robot.
    
    This class acts as the central coordinator for the weed detection application,
    handling user interactions and coordinating between different components.
    """
    def __init__(self, model: WeedDetectorModel, gui: WeedDetectorGUI):
        self.model = model
        self.gui = gui
        self.robot = Robot(gui, model)

        # Pass model reference to GUI for confidence updates
        self.gui.model = model

        model_name = os.path.basename(model.model_path)
        gui.model_info_var.set(f"Model: {model_name}")

        # Set Callbacks for GUI events
        self.gui.on_select_image = self.handle_select_image
        self.gui.on_detect = self.handle_detect
        self.gui.on_start_robot = self.handle_start_robot
        self.gui.on_stop_robot = self.handle_stop_robot

        # Optional: Model information display
        if hasattr(self.gui, "model_info_var"):
            self.gui.model_info_var.set(f"Model: {self.model.model_path}")

    def handle_select_image(self, file_path):
        """ will be called when the user selects an image file."""
        try:
            image = self.model.load_image(file_path)
            self.gui.display_image(image)
            # Start detection process after image is loaded
            self.handle_detect(file_path)
        except (ValueError, FileNotFoundError, OSError) as e:
            self.gui.show_error_box(f"Fehler beim Laden des Bildes: {e}")

    def handle_detect(self, file_path):
        """ will be called when the user clicks the detect button."""
        try:
            # Update model confidence from GUI slider
            confidence = self.gui.conf_var.get()
            self.model.model.conf = confidence

            image = self.model.load_image(file_path)
            # Perform detection using the model
            processed_image, result = self.model.detect_weeds(image)
            # Display the processed image and results in the GUI
            if processed_image is None:
                raise ValueError("Processed image is None, detection failed.")
            self.gui.display_image(processed_image)
            self.gui.update_results(f"Detection with confidence {confidence}: {result}")
        except (ValueError, FileNotFoundError, OSError, RuntimeError) as e:
            self.gui.show_error_box(f"Fehler bei der Erkennung: {e}")

    def handle_start_robot(self):
        """ will be called when the user clicks the start robot button."""
        try:
            self.robot.start_robot()
        except (RuntimeError, OSError) as e:
            self.gui.show_error_box(f"Fehler beim Starten des Roboters: {e}")

    def handle_stop_robot(self):
        """ will be called when the user clicks the stop robot button."""
        try:
            self.robot.stop_robot()
        except (RuntimeError, OSError) as e:
            self.gui.show_error_box(f"Fehler beim Stoppen des Roboters: {e}")

    def run(self):
        """Start GUI event loop."""
        self.gui.run()
