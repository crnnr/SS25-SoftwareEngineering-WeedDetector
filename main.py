""" Entry point for the Weed Detector application. This script initializes the GUI and loads the model. """
import os
from model import WeedDetectorModel
from gui import WeedDetectorGUI

def main():
    root = tk.Tk()
    
    possible_trained_models = [
        "runs/detect_train/weights/best.pt",
        "data/weights/best.pt", 
        "data/models/best.pt",
        "models/best.pt",
    ]
    
    model_path = "yolov8n.pt"
    
    for trained_path in possible_trained_models:
        if os.path.exists(trained_path):
            model_path = trained_path
            break
    
    if not os.path.exists(model_path):
        messagebox.showerror("Model Error", f"Model file '{model_path}' not found in the container.")
        print(f"Error: Model file '{model_path}' not found.")
        
        print("Files in current directory:")
        os.system("ls -la")
        print("\nFiles in data directory:")
        os.system("ls -la data/ 2>/dev/null || echo 'data/ directory not found'")
        print("\nFiles in models directory:")
        os.system("ls -la models/ 2>/dev/null || echo 'models/ directory not found'")
        print("\nFiles in runs directory:")
        os.system("ls -la runs/ 2>/dev/null || echo 'runs/ directory not found'")
        
        root.quit()
        return
    try:
        model = WeedDetectorModel(model_path=model_path)
    except Exception as e:
        messagebox.showerror("Model Error", f"Failed to load the model: {str(e)}")
        print(f"Error loading model: {e}")
        root.quit()
        return
    
    # Create the modern GUI
    app = WeedDetectorGUI(root, model)
    
    root.mainloop()

if __name__ == "__main__":
    main()