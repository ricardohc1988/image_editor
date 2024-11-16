import os
import io
from tkinter import filedialog, messagebox
from PIL import Image, ImageEnhance
import customtkinter as ctk
from rembg import remove
import threading

# Crear directorios si no existen
if not os.path.exists("images"):
    os.makedirs("images")
if not os.path.exists("output_images"):
    os.makedirs("output_images")
if not os.path.exists("backgrounds"):
    os.makedirs("backgrounds")

# Configuración de la interfaz de usuario con CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ImageEditorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Image Editor App")
        self.geometry("840x600")
        
        # Variables
        self.image = None
        self.image_path = None
        self.processed_image = None
        self.rotation_angle = 0
        self.selected_background = None
        
        # Frame izquierdo para los controles
        self.left_frame = ctk.CTkFrame(self, width=250)
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Espaciado interno general del frame
        self.left_frame.grid_rowconfigure(tuple(range(10)), weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        # Cargar imagen
        self.load_button = ctk.CTkButton(self.left_frame, text="Load Image", command=self.load_image)
        self.load_button.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        # Slider de brillo
        self.brightness_label = ctk.CTkLabel(self.left_frame, text="Brightness")
        self.brightness_label.grid(row=1, column=0, pady=(10, 5), padx=10, sticky="w")
        self.brightness_slider = ctk.CTkSlider(self.left_frame, from_=0.5, to=2, command=self.adjust_brightness)
        self.brightness_slider.set(1)
        self.brightness_slider.grid(row=2, column=0, pady=5, padx=10, sticky="ew")

        # Slider de contraste
        self.contrast_label = ctk.CTkLabel(self.left_frame, text="Contrast")
        self.contrast_label.grid(row=3, column=0, pady=(10, 5), padx=10, sticky="w")
        self.contrast_slider = ctk.CTkSlider(self.left_frame, from_=0.5, to=2, command=self.adjust_contrast)
        self.contrast_slider.set(1)
        self.contrast_slider.grid(row=4, column=0, pady=5, padx=10, sticky="ew")

        # Slider de saturación
        self.saturation_label = ctk.CTkLabel(self.left_frame, text="Saturation")
        self.saturation_label.grid(row=5, column=0, pady=(10, 5), padx=10, sticky="w")
        self.saturation_slider = ctk.CTkSlider(self.left_frame, from_=0.5, to=2, command=self.adjust_saturation)
        self.saturation_slider.set(1)
        self.saturation_slider.grid(row=6, column=0, pady=5, padx=10, sticky="ew")

        # Botón para eliminar fondo
        self.remove_bg_button = ctk.CTkButton(self.left_frame, text="Remove Background", command=self.start_remove_background)
        self.remove_bg_button.grid(row=7, column=0, pady=(15, 5), padx=10, sticky="ew")

        # Botón para rotar la imagen
        self.rotate_button = ctk.CTkButton(self.left_frame, text="Rotate 90°", command=self.rotate_image)
        self.rotate_button.grid(row=8, column=0, pady=(10, 5), padx=10, sticky="ew")

        # Dropdown para elegir el fondo
        self.background_label = ctk.CTkLabel(self.left_frame, text="Select Background")
        self.background_label.grid(row=9, column=0, pady=(15, 5), padx=10, sticky="w")
        self.background_menu = ctk.CTkOptionMenu(self.left_frame, values=self.load_background_images(), command=self.apply_background)
        self.background_menu.grid(row=10, column=0, pady=5, padx=10, sticky="ew")
        self.background_menu.configure(state="disabled")

        # Botón para guardar la imagen
        self.save_button = ctk.CTkButton(self.left_frame, text="Save Image", command=self.save_image)
        self.save_button.grid(row=11, column=0, pady=(10, 15), padx=10, sticky="ew")

        # Frame derecho para la imagen
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Área de imagen
        self.image_label = ctk.CTkLabel(self.right_frame, text="No Image Loaded", width=500, height=500)
        self.image_label.grid(row=0, column=0, padx=20, pady=20)

    def load_background_images(self):
        background_images = []
        for file_name in os.listdir("backgrounds"):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                background_images.append(file_name)
        return background_images

    def apply_background(self, selected_background):
        if self.image and selected_background:
            background_path = os.path.join("backgrounds", selected_background)
            background_image = Image.open(background_path).convert("RGBA")
            
            # Redimensionar el fondo al tamaño de la imagen
            background_image = background_image.resize(self.image.size, Image.Resampling.LANCZOS)
            
            # Poner la imagen procesada sobre el fondo
            background_image.paste(self.processed_image, (0, 0), self.processed_image)
            self.display_image(background_image)

            # Guardar el fondo seleccionado
            self.selected_background = background_image

    def load_image(self):
        self.image_path = filedialog.askopenfilename(initialdir="images", title="Select an Image",
                                                    filetypes=(("All files", "*.*"), ("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg")))

        if self.image_path:
            self.image = Image.open(self.image_path).convert("RGBA")
            self.processed_image = self.image
            self.display_image(self.image)
            self.remove_bg_button.configure(state="normal")
            self.image_label.configure(text="No Image Loaded")
            self.background_menu.configure(state="disabled")

    def start_remove_background(self):
        threading.Thread(target=self.remove_background).start()

    def remove_background(self):
        if self.image:
            self.remove_bg_button.configure(state="disabled")
            try:
                with open(self.image_path, "rb") as img_file:
                    img_data = img_file.read()
                    no_bg_data = remove(img_data)
                self.processed_image = Image.open(io.BytesIO(no_bg_data)).convert("RGBA")
                self.image = self.processed_image
                self.display_image(self.processed_image)

                # Habilitar el dropdown para elegir fondo después de eliminar el fondo
                self.background_menu.configure(state="normal")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove background: {e}")

    def adjust_brightness(self, value):
        self.apply_all_adjustments()

    def adjust_contrast(self, value):
        self.apply_all_adjustments()

    def adjust_saturation(self, value):
        self.apply_all_adjustments()

    def apply_all_adjustments(self):
        if self.image:
            adjusted_image = self.image
            brightness_value = self.brightness_slider.get()
            contrast_value = self.contrast_slider.get()
            saturation_value = self.saturation_slider.get()
            
            if brightness_value != 1:
                enhancer = ImageEnhance.Brightness(adjusted_image)
                adjusted_image = enhancer.enhance(brightness_value)
                self.processed_image = adjusted_image
            if contrast_value != 1:
                enhancer = ImageEnhance.Contrast(adjusted_image)
                adjusted_image = enhancer.enhance(contrast_value)
                self.processed_image = adjusted_image
            if saturation_value != 1:
                enhancer = ImageEnhance.Color(adjusted_image)
                adjusted_image = enhancer.enhance(saturation_value)
                self.processed_image = adjusted_image
            
            self.processed_image = adjusted_image
            
            # Aplicar el fondo si fue seleccionado
            if self.selected_background:
                self.apply_background_on_adjustment(self.selected_background)
            else:
                self.display_image(self.processed_image)

    def apply_background_on_adjustment(self, background_image):
        if self.processed_image and background_image:
            # Redimensionar el fondo al tamaño de la imagen procesada
            background_image_resized = background_image.resize(self.processed_image.size, Image.Resampling.LANCZOS)
            
            # Poner la imagen procesada sobre el fondo
            background_image_resized.paste(self.processed_image, (0, 0), self.processed_image)
            self.display_image(background_image_resized)

    def rotate_image(self):
        if self.processed_image:  # Asegúrate de rotar la imagen procesada
            self.rotation_angle = (self.rotation_angle + 90) % 360
            rotated_image = self.processed_image.rotate(self.rotation_angle, expand=True)
            self.processed_image = rotated_image
            self.display_image(rotated_image)

    def display_image(self, image):
        img = image.resize((500, 500), Image.Resampling.LANCZOS)
        img = ctk.CTkImage(img, size=(500, 500))
        self.image_label.configure(image=img)
        self.image_label.image = img

    def save_image(self):
        if self.processed_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if save_path:
                self.processed_image.save(save_path)
                messagebox.showinfo("Saved", f"Image saved to {save_path}")
        
if __name__ == "__main__":
    app = ImageEditorApp()
    app.mainloop()
