import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import filedialog
import cv2
import os
from model import WeedDetectorModel

def camera_capture(model):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Could not open camera. Check if camera is connected and accessible.")
        return
    cv2.namedWindow("Camera Capture Weed Detector", cv2.WINDOW_NORMAL)
    model_name = model.model_path
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            try:
                processed_frame = model.predict(frame)
                frame_h, frame_w = processed_frame.shape[:2]
                model_text = f"Model: {model_name}"
                text_size = cv2.getTextSize(model_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                cv2.putText(
                    processed_frame,
                    model_text,
                    (frame_w - text_size[0] - 10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
                )
                cv2.imshow("Camera Capture Weed Detector", processed_frame)
                key = cv2.waitKey(1)
                if key == 27 or cv2.getWindowProperty("Camera Capture Weed Detector", cv2.WND_PROP_VISIBLE) < 1:
                    break
            except Exception as e:
                print(f"Error processing frame: {e}")
                cv2.imshow("Camera Capture Weed Detector", frame)
                if cv2.waitKey(1) == 27:
                    break
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        for i in range(5):
            cv2.waitKey(1)

def process_image(model, file_path):
    print(f"Processing image from file path: {file_path}")
    try:
        processed_image = model.predict(file_path)
        model_name = model.model_path
        frame_h, frame_w = processed_image.shape[:2]
        model_text = f"Model: {model_name}"
        text_size = cv2.getTextSize(model_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        cv2.putText(
            processed_image,
            model_text,
            (frame_w - text_size[0] - 10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )
        cv2.namedWindow("Processed Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Processed Image", processed_image)
        print("Displaying processed image")
        while True:
            key = cv2.waitKey(100)
            if key == 27 or cv2.getWindowProperty("Processed Image", cv2.WND_PROP_VISIBLE) < 1:
                break
        cv2.destroyAllWindows()
        for i in range(5):
            cv2.waitKey(1)
    except Exception as e:
        print(f"Error in process_image: {e}")
        import traceback
        traceback.print_exc()
        messagebox.showerror("Error", f"Failed to process image: {str(e)}")

def show_custom_file_dialog(model):
    dialog = tk.Toplevel()
    dialog.title("Enter Image Path")
    dialog.geometry("600x150")
    dialog.configure(bg="lightgray")
    dialog.transient()
    dialog.grab_set()
    path_frame = tk.Frame(dialog, bg="lightgray")
    path_frame.pack(fill="x", padx=20, pady=20)
    path_label = tk.Label(path_frame, text="Image path:", bg="lightgray")
    path_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    path_entry = tk.Entry(path_frame, width=50)
    path_entry.grid(row=0, column=1, padx=5, pady=5)
    path_entry.insert(0, "/app/sample.jpg")
    button_frame = tk.Frame(dialog, bg="lightgray")
    button_frame.pack(fill="x", padx=20, pady=10)
    def on_process():
        file_path = path_entry.get().strip()
        dialog.destroy()
        if not file_path:
            messagebox.showerror("Error", "No file path provided")
            return
        if not (file_path.lower().endswith('.jpg') or \
                file_path.lower().endswith('.jpeg') or \
                file_path.lower().endswith('.png')):
            messagebox.showerror("Invalid File", "Please enter a valid image file path (jpg, jpeg, png)")
            return
        try:
            process_image(model, file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {str(e)}")
            print(f"Error processing image: {e}")
    process_btn = tk.Button(
        button_frame, text="Process Image", 
        bg="#4CAF50", fg="white", 
        command=on_process
    )
    process_btn.pack(side="left", padx=5)
    cancel_btn = tk.Button(
        button_frame, text="Cancel", 
        bg="#F44336", fg="white", 
        command=dialog.destroy
    )
    cancel_btn.pack(side="right", padx=5)
    dialog.wait_window()

def select_image(model):
    try:
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("JPEG files", "*.jpg"),
                ("JPEG files", "*.jpeg"), 
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            if not (
                file_path.lower().endswith('.jpg') or 
                file_path.lower().endswith('.jpeg') or 
                file_path.lower().endswith('.png')
            ):
                messagebox.showerror("Invalid File", "Please select a valid image file.")
                return
            process_image(model, file_path)
    except Exception as e:
        print(f"Standard file dialog failed: {e}. Using custom dialog instead.")
        show_custom_file_dialog(model)

def main():
    root = tk.Tk()
    root.title("Weed Detector")
    root.geometry("800x600")
    root.configure(bg="lightgray")
    root.resizable(False, False)
    
    # Check for trained models first
    possible_trained_models = [
        "runs/detect_train/weights/best.pt",
        "data/weights/best.pt", 
        "data/models/best.pt",
        "models/best.pt",
    ]
    
    model_path = "yolov8n.pt"  # Default model
    
    # Try to find a trained model
    for trained_path in possible_trained_models:
        if os.path.exists(trained_path):
            model_path = trained_path
            print(f"Found trained weed detection model at {trained_path}")
            break
    
    if not os.path.exists(model_path):
        messagebox.showerror("Model Error", f"Model file '{model_path}' not found in the container.")
        print(f"Error: Model file '{model_path}' not found.")
        
        # List all files and directories for debugging
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
    title_frame = tk.Frame(root, bg="lightgray")
    title_frame.pack(pady=20)
    title_label = tk.Label(title_frame, text="Weed Detector", font=("Arial", 24), bg="lightgray")
    title_label.pack()
    button_frame = tk.Frame(root, bg="lightgray")
    button_frame.pack(pady=20)
    button_width = 20
    button_height = 2
    button_font = ("Arial", 16, "bold")
    button_bg = "#4CAF50"
    button_fg = "white"
    button_active_bg = "#388E3C"
    select_image_button = tk.Button(
        button_frame, text="Select Image", font=button_font,
        width=button_width, height=button_height,
        bg=button_bg, fg=button_fg, activebackground=button_active_bg,
        relief=tk.RAISED, bd=3,
        command=lambda: select_image(model)
    )
    select_image_button.pack(side=tk.TOP, pady=10, fill=tk.X)
    set_resolution_button = tk.Button(
        button_frame, text="Set Resolution", font=button_font,
        width=button_width, height=button_height,
        bg=button_bg, fg=button_fg, activebackground=button_active_bg,
        relief=tk.RAISED, bd=3,
        command=lambda: messagebox.showinfo(
            "Resolution", "Set resolution functionality not implemented."
        )
    )
    set_resolution_button.pack(side=tk.TOP, pady=10, fill=tk.X)
    image_name_label = tk.Label(
        button_frame, text="Image Name:", font=("Arial", 16), bg="lightgray"
    )
    image_name_label.pack(side=tk.TOP, pady=10, fill=tk.X)
    camera_capture_button = tk.Button(
        button_frame, text="Camera Capture", font=button_font,
        width=button_width, height=button_height,
        bg=button_bg, fg=button_fg, activebackground=button_active_bg,
        relief=tk.RAISED, bd=3,
        command=lambda: camera_capture(model)
    )
    camera_capture_button.pack(side=tk.TOP, pady=10, fill=tk.X)
    save_image_button = tk.Button(
        button_frame, text="Save Image", font=button_font,
        width=button_width, height=button_height,
        bg=button_bg, fg=button_fg, activebackground=button_active_bg,
        relief=tk.RAISED, bd=3,
        command=lambda: messagebox.showinfo(
            "Save Image", "Save image functionality not implemented."
        )
    )
    save_image_button.pack(side=tk.TOP, pady=10, fill=tk.X)
    exit_button = tk.Button(
        button_frame, text="Exit", font=button_font,
        width=button_width, height=button_height,
        bg="#F44336", fg="white", activebackground="#B71C1C",
        relief=tk.RAISED, bd=3,
        command=root.quit
    )
    exit_button.pack(side=tk.TOP, pady=10, fill=tk.X)
    root.mainloop()

if __name__ == "__main__":
    main()