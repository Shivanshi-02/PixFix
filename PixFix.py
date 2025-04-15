import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk, ImageEnhance
import numpy as np
import colorsys

class ImageAdjuster:
    def __init__(self, master):
        self.master = master
        master.title("PixFix")
        master.configure(bg="#f0f0f0")

        self.image_path = None
        self.original_image = None
        self.processed_image = None
        self.image_tk = None

        self.brightness_value = tk.IntVar(value=0)
        self.contrast_value = tk.DoubleVar(value=0.0)
        self.saturation_value = tk.DoubleVar(value=0.0)
        self.hue_value = tk.IntVar(value=0)

        self.button_style = {
            "bg": "#4c8bf5",  # Blue color
            "fg": "white",
            "padx": 15,
            "pady": 8,
            "font": ("Arial", 10, "bold"),
            "relief": tk.RAISED,
            "bd": 2,
            "borderwidth": 3,
            "highlightthickness": 0,
            "activebackground": "#66a5ff",
            "activeforeground": "white",
        }
        self.download_button_style = self.button_style.copy()
        self.download_button_style["bg"] = "#e74c3c"  # Red color for download
        self.download_button_style["activebackground"] = "#ff6a5a"

        self.create_widgets()

    def create_widgets(self):
        # Image Upload Box (Larger Dimensions, Resizable)
        self.image_label_frame = tk.LabelFrame(self.master, text="Uploaded Image", padx=10, pady=10, bg="white", relief=tk.GROOVE)
        self.image_label = tk.Label(self.image_label_frame, text="No image loaded", width=40, height=10, bg="lightgray")
        self.image_label.pack(pady=10, padx=10, fill="both", expand=True)
        self.image_label_frame.pack(pady=15, padx=15, fill="both", expand=True) # Expand frame

        # Load Image Button
        load_button = tk.Button(self.master, text="Load Image", command=self.load_image, bg="#2ecc71", fg="white", padx=15, pady=8, font=("Arial", 10, "bold"), relief=tk.RAISED, bd=2, borderwidth=3, highlightthickness=0, activebackground="#48c785", activeforeground="white")
        load_button.pack(pady=(0, 20)) # Increased space below the button

        # Brightness Slider
        brightness_frame = tk.Frame(self.master, bg="#f0f0f0")
        tk.Label(brightness_frame, text="Brightness:", font=("Arial", 10), bg="#f0f0f0").pack(side=tk.LEFT, padx=(15, 5))
        self.brightness_slider = tk.Scale(brightness_frame, from_=-100, to=100, orient=tk.HORIZONTAL,
                                         variable=self.brightness_value, command=self.adjust_image,
                                         bg="#ddd", fg="black", highlightthickness=1, relief=tk.FLAT)
        self.brightness_slider.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        brightness_frame.pack(fill="x", padx=15, pady=5) # Consistent vertical space

        # Contrast Slider
        contrast_frame = tk.Frame(self.master, bg="#f0f0f0")
        tk.Label(contrast_frame, text="Contrast:", font=("Arial", 10), bg="#f0f0f0").pack(side=tk.LEFT, padx=(15, 5))
        self.contrast_slider = tk.Scale(contrast_frame, from_=-2.0, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, # Adjusted range
                                       variable=self.contrast_value, command=self.adjust_image,
                                       bg="#ddd", fg="black", highlightthickness=1, relief=tk.FLAT)
        self.contrast_slider.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        contrast_frame.pack(fill="x", padx=15, pady=5) # Consistent vertical space

        # Saturation Slider
        saturation_frame = tk.Frame(self.master, bg="#f0f0f0")
        tk.Label(saturation_frame, text="Saturation:", font=("Arial", 10), bg="#f0f0f0").pack(side=tk.LEFT, padx=(15, 5))
        self.saturation_slider = tk.Scale(saturation_frame, from_=-2.0, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, # Adjusted range
                                         variable=self.saturation_value, command=self.adjust_image,
                                         bg="#ddd", fg="black", highlightthickness=1, relief=tk.FLAT)
        self.saturation_slider.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        saturation_frame.pack(fill="x", padx=15, pady=5) # Consistent vertical space

        # Hue Slider
        hue_frame = tk.Frame(self.master, bg="#f0f0f0")
        tk.Label(hue_frame, text="Hue:", font=("Arial", 10), bg="#f0f0f0").pack(side=tk.LEFT, padx=(15, 5))
        self.hue_slider = tk.Scale(hue_frame, from_=-180, to=180, orient=tk.HORIZONTAL,
                                  variable=self.hue_value, command=self.adjust_image,
                                  bg="#ddd", fg="black", highlightthickness=1, relief=tk.FLAT)
        self.hue_slider.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        hue_frame.pack(fill="x", padx=15, pady=5) # Consistent vertical space

        # Action Buttons Frame (Middle Alignment)
        action_frame = tk.Frame(self.master, bg="#f0f0f0")
        resize_button = tk.Button(action_frame, text="Resize", command=self.ask_resize, **self.button_style)
        resize_button.pack(side=tk.LEFT, padx=5)
        reset_button = tk.Button(action_frame, text="Reset", command=self.reset_image, bg="#f44336", fg="white", padx=15, pady=8, font=("Arial", 10, "bold"), relief=tk.RAISED, bd=2, borderwidth=3, highlightthickness=0, activebackground="#ff7961", activeforeground="white")
        reset_button.pack(side=tk.LEFT, padx=5)
        rotate_button = tk.Button(action_frame, text="Rotate", command=self.rotate_image, **self.button_style)
        rotate_button.pack(side=tk.LEFT, padx=5)
        download_button = tk.Button(action_frame, text="Download", command=self.save_image, **self.download_button_style)
        download_button.pack(side=tk.LEFT, padx=5)
        action_frame.pack(pady=20) # Increased space below buttons

        # Configure weight for the main window to center the content horizontally and vertically
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1) # Allow image frame to expand vertically

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if self.image_path:
            try:
                self.original_image = Image.open(self.image_path).convert("RGB")
                self.processed_image = self.original_image.copy()
                self.update_image_display()
                self.reset_sliders()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not open image: {e}")

    def adjust_image(self, event=None):
        if self.original_image:
            brightness = self.brightness_value.get() / 100.0
            contrast = self.contrast_value.get()
            saturation = self.saturation_value.get()
            hue_offset = self.hue_value.get() / 360.0  # Normalize hue to 0-1

            img = self.original_image.copy()

            pixels = img.load()
            width, height = img.size

            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

                    # Adjust Brightness (Value)
                    v = max(0, min(1, v + brightness))

                    # Adjust Hue
                    h = (h + hue_offset) % 1.0

                    # Convert back to RGB
                    r_out, g_out, b_out = colorsys.hsv_to_rgb(h, s, v)
                    pixels[x, y] = (int(r_out * 255), int(g_out * 255), int(b_out * 255))

            # Adjust Contrast and Saturation AFTER HSV adjustments
            enhancer_contrast = ImageEnhance.Contrast(img)
            img = enhancer_contrast.enhance(1 + contrast)

            enhancer_saturation = ImageEnhance.Color(img)
            img = enhancer_saturation.enhance(1 + saturation)

            self.processed_image = img
            self.update_image_display()

    def ask_resize(self):
        if self.original_image:
            dialog = tk.Toplevel(self.master)
            dialog.title("Resize Image")

            # Width Input
            width_frame = tk.Frame(dialog)
            width_frame.pack(pady=5, padx=10)
            width_label = tk.Label(width_frame, text="New Width:")
            width_label.pack(side=tk.LEFT)
            width_entry = tk.Entry(width_frame)
            width_entry.insert(0, str(self.processed_image.width))
            width_entry.pack(side=tk.LEFT)

            # Height Input
            height_frame = tk.Frame(dialog)
            height_frame.pack(pady=5, padx=10)
            height_label = tk.Label(height_frame, text="New Height:")
            height_label.pack(side=tk.LEFT)
            height_entry = tk.Entry(height_frame)
            height_entry.insert(0, str(self.processed_image.height))
            height_entry.pack(side=tk.LEFT)

            def perform_resize():
                try:
                    width = int(width_entry.get())
                    height = int(height_entry.get())
                    if width > 0 and height > 0:
                        self.processed_image = self.processed_image.resize((width, height), Image.Resampling.LANCZOS)
                        self.update_image_display()
                        dialog.destroy()
                    else:
                        messagebox.showerror("Error", "Width and height must be positive integers.")
                except ValueError:
                    messagebox.showerror("Error", "Invalid width or height.")

            resize_button = tk.Button(dialog, text="Resize", command=perform_resize, **self.button_style)
            resize_button.pack(pady=10)

            dialog.transient(self.master)
            self.master.wait_window(dialog)

    def rotate_image(self):
        if self.original_image:
            angle = simpledialog.askinteger("Rotate", "Enter rotation angle (degrees):", initialvalue=0)
            if angle is not None:
                self.processed_image = self.processed_image.rotate(-angle, expand=False, fill=(0, 0, 0)) # Rotate without expanding and fill black
                self.update_image_display()

    def reset_image(self):
        if self.original_image:
            self.processed_image = self.original_image.copy()
            self.update_image_display()
            self.reset_sliders()

    def save_image(self):
        if self.processed_image:
            filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                                   filetypes=[("PNG files", "*.png"),
                                                              ("JPEG files", "*.jpg;*.jpeg"),
                                                              ("GIF files", "*.gif"),
                                                              ("BMP files", "*.bmp"),
                                                              ("All files", "*.*")])
            if filepath:
                try:
                    self.processed_image.save(filepath)
                    messagebox.showinfo("Save Successful", f"Image saved to {filepath}")
                except Exception as e:
                    messagebox.showerror("Save Error", f"Could not save image: {e}")
        else:
            messagebox.showerror("Error", "No image to save.")

    def reset_sliders(self):
        self.brightness_value.set(0)
        self.contrast_value.set(0.0)
        self.saturation_value.set(0.0)
        self.hue_value.set(0)
        self.brightness_slider.set(0)
        self.contrast_slider.set(0.0)
        self.saturation_slider.set(0.0)
        self.hue_slider.set(0)

    def update_image_display(self):
        if self.processed_image:
            box_width = self.image_label.winfo_width()
            box_height = self.image_label.winfo_height()

            if box_width > 1 and box_height > 1: # Ensure box dimensions are available
                img_width, img_height = self.processed_image.size

                width_ratio = box_width / img_width
                height_ratio = box_height / img_height

                if width_ratio < 1 or height_ratio < 1: # Image is larger than the box
                    if width_ratio < height_ratio:
                        new_width = int(img_width * width_ratio)
                        new_height = int(img_height * width_ratio)
                    else:
                        new_width = int(img_width * height_ratio)
                        new_height = int(img_height * height_ratio)
                    resized_image = self.processed_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    self.image_tk = ImageTk.PhotoImage(resized_image)
                    self.image_label.config(image=self.image_tk, text="")
                    self.image_label.image = self.image_tk
                else: # Image fits within the box
                    self.image_tk = ImageTk.PhotoImage(self.processed_image)
                    self.image_label.config(image=self.image_tk, text="")
                    self.image_label.image = self.image_tk
            else:
                # If box dimensions are not yet available, just load the original (it will resize on next update)
                self.image_tk = ImageTk.PhotoImage(self.processed_image)
                self.image_label.config(image=self.image_tk, text="")
                self.image_label.image = self.image_tk
        else:
            self.image_label.config(text="No image loaded", image="")

if __name__ == "__main__":
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1) # Allow image frame to expand vertically
    app = ImageAdjuster(root)
    root.mainloop()