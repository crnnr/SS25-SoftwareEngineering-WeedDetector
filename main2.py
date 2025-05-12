"""Main script for the project."""
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import filedialog
import os
import cv2
from ultralytics import YOLO

def camera_capture(model):
    """Function to capture an image from the camera."""
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret: break

        results = model.predict(source=frame, conf=0.25)
        for r in results:
            for box in r.boxes:
                x1,y1,x2,y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                score = box.conf[0]
                cx, cy = (x1+x2)//2, (y1+y2)//2

                name = model.names[cls_id]
                cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0),2)
                cv2.circle(frame,(cx,cy),5,(0,0,255),-1)
                cv2.putText(frame, f"{name} {score:.2f}", (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0),2)

        cv2.imshow("Camera Capture Weed Detector", frame)
        if cv2.waitKey(1)==27: break

    cap.release()
    cv2.destroyAllWindows()

def process_image(model, image):
    """Function to process the selected image."""
    # Perform detection
    results = model.predict(source=image, conf=0.25)
    # Process results (this is just a placeholder)
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls[0])
            score = box.conf[0]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            name = model.names[cls_id]
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(image, (cx, cy), 5, (0, 0, 255), -1)
            cv2.putText(image, f"{name} {score:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
     

def select_image():
    """Function to select an image file."""
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=(("Image Files", "*.jpg;*.jpeg;*.png"), ("All Files", "*.*"))
    )
    if file_path:
        # Check if the selected file is a valid image
        if not (file_path.endswith('.jpg') or file_path.endswith('.jpeg') or file_path.endswith('.png')):
            messagebox.showerror("Invalid File", "Please select a valid image file.")
            return
        # Process the image (placeholder for actual processing)
        process_image(file_path)

def main():
    root = tk.Tk()
    root.title("Weed Detector")
    root.geometry("600x400")
    root.configure(bg="lightgray")
    root.resizable(False, False)

    # Load the YOLO model
    model = YOLO("yolov8n.pt")
    # Check if the model is loaded successfully
    if model is None:
        messagebox.showerror("Model Error", "Failed to load the YOLO model.")
        return

    # Create a frame for the title
    title_frame = tk.Frame(root, bg="white")
    title_frame.pack(pady=20)
    title_label = tk.Label(title_frame, text="Weed Detector", font=("Arial", 24), bg="lightgray")
    title_label.pack()
    # Create a frame for the buttons
    button_frame = tk.Frame(root, bg="white")
    button_frame.pack(pady=20)
    # Create a button to select an image
    select_image_button = tk.Button(button_frame, text="Select Image", font=("Arial", 16), command=select_image)
    select_image_button.pack(side=tk.TOP, pady=10)

    #Create a button to set resolution
    set_resolution_button = tk.Button(button_frame, text="Set Resolution", font=("Arial", 16), command=lambda: messagebox.showinfo("Resolution", "Set resolution functionality not implemented."))
    set_resolution_button.pack(side=tk.TOP, pady=10)

    #Create a text field for image name
    image_name_label = tk.Label(button_frame, text="Image Name:", font=("Arial", 16), bg="lightgray")
    image_name_label.pack(side=tk.TOP, pady=10)
    image_name_entry = tk.Entry(button_frame, font=("Arial", 16))

    # Create a button for camera capture
    camera_capture_button = tk.Button(button_frame, text="Camera Capture", font=("Arial", 16), command=lambda: camera_capture(model))
    camera_capture_button.pack(side=tk.TOP, pady=10)

    # Create a button to save the image
    save_image_button = tk.Button(button_frame, text="Save Image", font=("Arial", 16), command=lambda: messagebox.showinfo("Save Image", "Save image functionality not implemented."))
    save_image_button.pack(side=tk.TOP, pady=10)

    # Create a button to exit the application
    exit_button = tk.Button(button_frame, text="Exit", font=("Arial", 16), command=root.quit)
    exit_button.pack(side=tk.TOP, pady=10)
    # Create a label to display instructions
    instructions_label = tk.Label(root, text="Select an image to process.", font=("Arial", 16), bg="lightgray")
    instructions_label.pack(pady=10)
    # Start the main loop

    root.mainloop()


if __name__ == "__main__":
    main()