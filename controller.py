from model import WeedDetectorModel
from gui import WeedDetectorGUI

class WeedDetectorController:
    def __init__(self, model: WeedDetectorModel, gui: WeedDetectorGUI):
        self.model = model
        self.gui = gui

        # Set Callbacks for GUI events
        self.gui.on_select_image = self.handle_select_image
        self.gui.on_detect = self.handle_detect

        # Optional: Model information display
        if hasattr(self.gui, "model_info_var"):
            self.gui.model_info_var.set(f"Model: {self.model.model_path}")

    def handle_select_image(self, file_path):
        """Wird aufgerufen, wenn der Nutzer ein Bild auswählt."""
        try:
            image = self.model.load_image(file_path)
            self.gui.display_image(image)
            # Start detection process after image is loaded
            self.handle_detect(file_path)
        except Exception as e:
            self.gui.show_error_box(f"Fehler beim Laden des Bildes: {e}")

    def handle_detect(self, file_path):
        """Wird aufgerufen, wenn der Nutzer die Erkennung startet."""
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

    def run(self):
        self.gui.run()