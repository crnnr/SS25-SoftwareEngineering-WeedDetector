""" Entry point for the Weed Detector application. This script initializes the GUI and loads the model. """
from controller import WeedDetectorController
from model import WeedDetectorModel
from gui import WeedDetectorGUI

def main():
    """Main function to run the Weed Detector application."""
    # Initialize the model
    model = WeedDetectorModel()

    # Initialize the GUI with the model
    gui = WeedDetectorGUI(model)

    # Create the controller to handle interactions between model and GUI
    controller = WeedDetectorController(model, gui)

    # Run the GUI application
    controller.run()

if __name__ == "__main__":
    main()