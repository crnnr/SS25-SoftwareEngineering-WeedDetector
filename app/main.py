""" Entry point for the Weed Detector application. This initializes the GUI and loads the model. """
from app.controller import WeedDetectorController
from app.model import WeedDetectorModel
from app.gui import WeedDetectorGUI


def main():
    """Main function to run the Weed Detector application."""
    # Initialize the model
    model = WeedDetectorModel()

    # Initialize the GUI with the model
    gui = WeedDetectorGUI()

    # Create the controller to handle interactions between model and GUI
    controller = WeedDetectorController(model, gui)

    # Run the GUI application
    controller.run()

if __name__ == "__main__":
    main()
