from model import WeedDetectorModel
from gui import WeedDetectorGUI
from robot import Robot
import os

class WeedDetectorController:
    def __init__(self, model: WeedDetectorModel, gui: WeedDetectorGUI):
        self.model = model
        self.gui = gui
        self.robot = Robot(gui, model)

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
        except Exception as e:
            self.gui.show_error_box(f"Fehler beim Laden des Bildes: {e}")

    def handle_detect(self, file_path):
        """ will be called when the user clicks the detect button."""
        try:
            image = self.model.load_image(file_path)
            # Perform detection using the model
            processed_image, result = self.model.detect_weeds(image)
            # Display the processed image and results in the GUI
            if processed_image is None:
                raise ValueError("Processed image is None, detection failed.")
            self.gui.display_image(processed_image)
            self.gui.update_results(result)
        except Exception as e:
            self.gui.show_error_box(f"Fehler bei der Erkennung: {e}")

    def handle_start_robot(self):
        """ will be called when the user clicks the start robot button."""
        try:
            self.robot.start_robot()
        except Exception as e:
            self.gui.show_error_box(f"Fehler beim Starten des Roboters: {e}")

    def handle_stop_robot(self):
        """ will be called when the user clicks the stop robot button."""
        try:
            self.robot.stop_robot()
        except Exception as e:
            self.gui.show_error_box(f"Fehler beim Stoppen des Roboters: {e}")

    def run(self):
        self.gui.run()