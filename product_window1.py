import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

class ProductWindow(tk.Toplevel):
    def __init__(self, parent, catalog_app):
        super().__init__(parent)
        self.catalog_app = catalog_app
        self.title("Agregar Producto")
        self.geometry("400x500")
        self.resizable(False, False)

        # Estilo de fuente y diseño
        self.font = ("Helvetica", 12)

        # Campos de entrada con etiquetas
        self.name_label = tk.Label(self, text="Nombre:", font=self.font)
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self, font=self.font)
        self.name_entry.pack(pady=5)

        self.desc_label = tk.Label(self, text="Descripción:", font=self.font)
        self.desc_label.pack(pady=5)
        self.desc_entry = tk.Entry(self, font=self.font)
        self.desc_entry.pack(pady=5)

        self.price_label = tk.Label(self, text="Precio:", font=self.font)
        self.price_label.pack(pady=5)
        self.price_entry = tk.Entry(self, font=self.font)
        self.price_entry.pack(pady=5)

        self.image_url_label = tk.Label(self, text="URL de Imagen (opcional):", font=self.font)
        self.image_url_label.pack(pady=5)
        self.image_url_entry = tk.Entry(self, font=self.font)
        self.image_url_entry.pack(pady=5)

        # Área para mostrar la imagen previa
        self.image_preview_label = tk.Label(self)
        self.image_preview_label.pack(pady=10)

        # Botón para guardar el producto
        self.save_button = tk.Button(self, text="Guardar", font=self.font, command=self.save_product)
        self.save_button.pack(pady=20)

        # Actualizar vista previa de la imagen cuando se ingrese una URL
        self.image_url_entry.bind("<KeyRelease>", self.update_image_preview)

    def update_image_preview(self, event=None):
        """Mostrar vista previa de la imagen basada en la URL"""
        image_url = self.image_url_entry.get()
        if image_url:
            try:
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                img.thumbnail((100, 100))  # Ajustar el tamaño de la imagen
                img_tk = ImageTk.PhotoImage(img)
                self.image_preview_label.config(image=img_tk)
                self.image_preview_label.image = img_tk
            except Exception as e:
                self.image_preview_label.config(image="")
                messagebox.showwarning("Error", "No se pudo cargar la imagen.")
        else:
            self.image_preview_label.config(image="")

    def save_product(self):
        """Guardar el producto nuevo"""
        name = self.name_entry.get()
        description = self.desc_entry.get()
        price = self.price_entry.get()
        image_url = self.image_url_entry.get()

        if not name or not description or not price:
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")
            return

        try:
            price = float(price)
        except ValueError:
            messagebox.showwarning("Error", "El precio debe ser un número.")
            return

        new_product = {
            "id_producto": len(self.catalog_app.products) + 1,
            "nombre": name,
            "descripcion": description,
            "id_usuario": 1,  # Asumiendo un id de usuario ficticio
            "estado": "si",  # Estado predeterminado
            "precio": price
        }

        if image_url:
            new_product["imagen_url"] = image_url

        self.catalog_app.add_product(new_product)
        self.destroy()  # Cerrar la ventana
