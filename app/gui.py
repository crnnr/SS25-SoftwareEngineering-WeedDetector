"""Weed Detection GUI using Tkinter and OpenCV"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import threading
import os

class WeedDetectorGUI:
    def __init__(self):
        """Initialize the Weed Detector GUI."""
        self.root = tk.Tk()
        self.cap = None
        
        self.root.title("Weed Detector")
        self.root.geometry("1200x900")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(True, True)
        
        # Create main layout
        self.create_layout()
        
    def create_layout(self):
        """Create the main layout of the GUI."""
        # Header frame
        header_frame = tk.Frame(self.root, bg="#34495e", height=80)
        header_frame.pack(fill="x", padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="Weed Detection System", 
            font=("Arial", 24, "bold"),
            bg="#34495e", 
            fg="#ecf0f1"
        )
        title_label.pack(pady=20)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#2c3e50")
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Left panel - Controls
        self.create_control_panel(content_frame)
        
        # Right panel - Image display
        self.create_display_panel(content_frame)
        
        # Bottom panel - Status and results
        self.create_status_panel()

        # Create robot status panel
        self.create_robot_status_panel()
        
    def create_control_panel(self, parent):
        """Create the control panel for image selection and camera controls."""
        control_frame = tk.Frame(parent, bg="#34495e", width=300)
        control_frame.pack(side="left", fill="y", padx=(0, 10))
        control_frame.pack_propagate(False)
        self.camera_running = False

        self.on_select_image = None # Callback for image selection
        self.on_detect = None # Callback for detection
        self.on_start_robot = None  # Callback for robot start
        self.on_stop_robot = None  # Callback for robot stop

        self.model_info_var = tk.StringVar(value="Model: Not loaded")
        
        # Control panel title
        control_title = tk.Label(
            control_frame,
            text="Controls",
            font=("Arial", 18, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        )
        control_title.pack(pady=20)
        
        # Image selection button
        self.select_btn = tk.Button(
            control_frame,
            text="Select Image",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            relief=tk.RAISED,
            bd=3,
            height=2,
            command=self.select_image
        )
        self.select_btn.pack(fill="x", padx=20, pady=10)
        
        # Camera button
        self.camera_btn = tk.Button(
            control_frame,
            text="Start Camera",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            relief=tk.RAISED,
            bd=3,
            height=2,
            command=self.toggle_camera
        )
        self.camera_btn.pack(fill="x", padx=20, pady=10)

        # Robot control button
        self.robot_btn = tk.Button(
            control_frame,
            text="Start Robot",
            font=("Arial", 12, "bold"),
            bg="red",
            fg="white",
            activebackground="#e67e22",
            relief=tk.RAISED,
            bd=3,
            height=2,
            command=self.start_robot
        )
        self.robot_btn.pack(fill="x", padx=20, pady=10)
        
        # Model info frame
        model_frame = tk.LabelFrame(
            control_frame,
            text="Model Information",
            font=("Arial", 10, "bold"),
            bg="#34495e",
            fg="#ecf0f1",
            relief=tk.RAISED,
            bd=2
        )
        model_frame.pack(fill="x", padx=20, pady=20)
        
        self.model_info_var = tk.StringVar(value="Model: Not loaded")
        model_info = tk.Label(
            model_frame,
            textvariable=self.model_info_var,
            font=("Arial", 9),
            bg="#34495e",
            fg="#bdc3c7",
            wraplength=250
        )
        model_info.pack(padx=10, pady=10)
        
        settings_frame = tk.LabelFrame(
            control_frame,
            text="Detection Settings",
            font=("Arial", 10, "bold"),
            bg="#34495e",
            fg="#ecf0f1",
            relief=tk.RAISED,
            bd=2
        )
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(settings_frame, text="Confidence:", bg="#34495e", fg="#bdc3c7").pack(anchor="w", padx=10)
        self.conf_var = tk.DoubleVar(value=0.15)
        conf_scale = tk.Scale(
            settings_frame,
            from_=0.05,
            to=0.95,
            resolution=0.05,
            orient="horizontal",
            variable=self.conf_var,
            bg="#34495e",
            fg="#ecf0f1",
            highlightbackground="#34495e"
        )
        conf_scale.pack(fill="x", padx=10, pady=5)
        
    def create_display_panel(self, parent):
        """Create the display panel for showing images and results."""
        display_frame = tk.Frame(parent, bg="#34495e")
        display_frame.pack(side="right", fill="both", expand=True)
        
        display_title = tk.Label(
            display_frame,
            text="Image Display",
            font=("Arial", 18, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        )
        display_title.pack(pady=10)
        
        canvas_frame = tk.Frame(display_frame, bg="#2c3e50", relief=tk.SUNKEN, bd=3)
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#2c3e50", highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.canvas.create_text(
            400, 300,
            text="Select an image or start camera to begin detection",
            font=("Arial", 16),
            fill="#7f8c8d",
            tags="placeholder"
        )
        
    def create_status_panel(self):
        """Create the status panel for displaying detection results."""
        status_frame = tk.Frame(self.root, bg="#34495e", height=120)
        status_frame.pack(fill="x", padx=10, pady=(0, 10))
        status_frame.pack_propagate(False)
        
        status_title = tk.Label(
            status_frame,
            text="Detection Results",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        )
        status_title.pack(anchor="w", padx=10, pady=5)
        
        results_frame = tk.Frame(status_frame, bg="#34495e")
        results_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.results_text = tk.Text(
            results_frame,
            height=4,
            bg="#2c3e50",
            fg="#ecf0f1",
            font=("Consolas", 10),
            relief=tk.SUNKEN,
            bd=2,
            state=tk.DISABLED
        )
        results_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_text.pack(side="left", fill="both", expand=True)
        results_scrollbar.pack(side="right", fill="y")

    def create_robot_status_panel(self):
        """Create the panel for displaying robot actions."""
        robot_status_frame = tk.Frame(self.root, bg="#34495e", height=120)
        robot_status_frame.pack(fill="x", padx=10, pady=(0, 10))
        robot_status_frame.pack_propagate(False)

        robot_status_title = tk.Label(
            robot_status_frame,
            text="Robot Actions",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        )
        robot_status_title.pack(anchor="w", padx=10, pady=5)

        robot_results_frame = tk.Frame(robot_status_frame, bg="#34495e")
        robot_results_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.robot_actions_text = tk.Text(
            robot_results_frame,
            height=4,
            bg="#2c3e50",
            fg="#ecf0f1",
            font=("Consolas", 10),
            relief=tk.SUNKEN,
            bd=2,
            state=tk.DISABLED
        )
        robot_status_scrollbar = ttk.Scrollbar(robot_results_frame, orient="vertical", command=self.results_text.yview)
        self.robot_actions_text.configure(yscrollcommand=robot_status_scrollbar.set)
        
        self.robot_actions_text.pack(side="left", fill="both", expand=True)
        robot_status_scrollbar.pack(side="right", fill="y")
        
    def update_results(self, message):
        """Update the results text area with a new message."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
        
    def clear_results(self):
        """Clear the results text area."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        
    def display_image(self, cv_image):
        """Display an OpenCV image in the Tkinter canvas."""
        if len(cv_image.shape) == 3:
            rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        else:
            rgb_image = cv_image
            
        pil_image = Image.fromarray(rgb_image)
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width, canvas_height = 800, 600
            
        img_width, img_height = pil_image.size
        
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y, 1.0)  # Don't upscale
        
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        display_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        self.photo = ImageTk.PhotoImage(display_image)
        
        self.canvas.delete("all")
        self.canvas.configure(scrollregion=(0, 0, new_width, new_height))
        self.canvas.create_image(new_width//2, new_height//2, image=self.photo)
        
    def select_image(self):
        """Open a file dialog to select an image and process it."""
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        
        if file_path and self.on_select_image:
            self.on_select_image(file_path)

    def process_image(self, file_path):
        """Process the selected image using the model."""
        if self.on_detect:
            self.on_detect(file_path)
            
    def toggle_camera(self):
        """Toggle the camera on or off."""
        if not self.camera_running:
            self.start_camera()
        else:
            self.stop_camera()
            
    def start_camera(self):
        """Start the camera for real-time detection."""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Camera Error", "Could not open camera.")
                return
                
            self.camera_running = True
            self.camera_btn.config(text="⏹ Stop Camera", bg="#e74c3c")
            self.select_btn.config(state=tk.DISABLED)
            
            self.clear_results()
            self.update_results("Camera started - Real-time detection active")
            
            self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
            self.camera_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
            
    def stop_camera(self):
        """Stop the camera and release resources."""
        self.camera_running = False
        if self.cap:
            self.cap.release()
            
        self.camera_btn.config(text="📷 Start Camera", bg="#27ae60")
        self.select_btn.config(state=tk.NORMAL)
        self.update_results("Camera stopped")
        
    def camera_loop(self):
        """Loop to read frames from the camera and process them."""
        while self.camera_running:
            if self.cap is None:
                break
                
            ret, frame = self.cap.read()
            if not ret:
                break
                
            try:
                # Update model confidence from slider
                if hasattr(self, 'model') and self.model:
                    self.model.model.conf = self.conf_var.get()
                
                if hasattr(self.model, 'detected_centers'):
                    self.model.detected_centers = []
                    
                processed_frame = self.model.predict(frame)
                
                self.root.after(0, self.display_image, processed_frame)
                
                if hasattr(self.model, 'detected_centers') and self.model.detected_centers:
                    result_msg = f"Live: {len(self.model.detected_centers)} object(s) detected"
                    self.root.after(0, self.update_live_results, result_msg)
                    
            except Exception as e:
                print(f"Error processing frame: {e}")
                
        if self.cap:
            self.cap.release()

    def start_robot(self):
        """Start the robot in demo mode."""
        if hasattr(self, "on_start_robot") and callable(self.on_start_robot):
            self.on_start_robot()
            self.robot_btn.config(text="Stop Robot", bg="#e74c3c", command=self.stop_robot)
        else:
            self.log_robot_action("Robot started (Demo-Modus)")
            self.robot_btn.config(text="Stop Robot", bg="#e74c3c", command=self.stop_robot)
    
    def stop_robot(self):
        if hasattr(self, "on_stop_robot") and callable(self.on_stop_robot):
            self.on_stop_robot()
            self.robot_btn.config(text="Start Robot", bg="#f39c12", command=self.start_robot)
        else:
            self.log_robot_action("Robot stopped (Demo-Modus)")
            self.robot_btn.config(text="Start Robot", bg="#f39c12", command=self.start_robot)

    def log_robot_action(self, message):
        """Append a robot action to the robot actions panel."""
        self.robot_actions_text.config(state=tk.NORMAL)
        self.robot_actions_text.insert(tk.END, message + "\n")
        self.robot_actions_text.see(tk.END)
        self.robot_actions_text.config(state=tk.DISABLED)
            
    def update_live_results(self, message):
        """Update the results text area with live detection results."""
        if self.camera_running:
            self.results_text.config(state=tk.NORMAL)
            lines = self.results_text.get(1.0, tk.END).strip().split('\n')
            if lines and 'Camera started' in lines[0]:
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, lines[0] + "\n")
            self.results_text.insert(tk.END, message + "\n")
            self.results_text.see(tk.END)
            self.results_text.config(state=tk.DISABLED)

    def show_error_box(self, message):
        """Show an error message box."""
        messagebox.showerror("Error", message)
        self.update_results(f"Error: {message}")

    def run(self):
        """Run the main loop of the GUI."""
        self.root.mainloop()