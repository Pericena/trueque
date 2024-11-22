import tkinter as tk
from tkinter import messagebox
import json
from product_window import ProductWindow
from utils import load_products, save_product
from PIL import Image, ImageTk
import requests
from io import BytesIO

class CatalogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Catálogo de Productos")
        self.root.geometry("800x600")
        
        # Cargar productos desde el archivo JSON
        self.products = load_products()

        # Crear un marco para mostrar los productos
        self.products_frame = tk.Frame(root)
        self.products_frame.pack(pady=20)

        # Botón para agregar nuevo producto
        self.add_button = tk.Button(root, text="Agregar Producto", command=self.open_add_window)
        self.add_button.pack(pady=10)

        self.update_product_list()

    def update_product_list(self):
        """Actualizar la visualización de productos en estilo "card"."""
        for widget in self.products_frame.winfo_children():
            widget.destroy()  # Limpiar el marco de productos
        
        for product in self.products:
            product_card = tk.Frame(self.products_frame, relief="solid", borderwidth=2, width=250, height=350)
            product_card.grid_propagate(False)  # Evitar que cambie el tamaño del Frame
            product_card.grid(row=self.products.index(product)//3, column=self.products.index(product)%3, padx=10, pady=10)

            # Imagen del producto
            image_label = tk.Label(product_card)
            image_label.pack(pady=5)

            if 'imagen_url' in product:
                try:
                    response = requests.get(product['imagen_url'])
                    img = Image.open(BytesIO(response.content))
                    img.thumbnail((150, 150))  # Ajustar el tamaño de la imagen
                    img_tk = ImageTk.PhotoImage(img)
                    image_label.config(image=img_tk)
                    image_label.image = img_tk
                except Exception as e:
                    image_label.config(text="Imagen no disponible")

            # Nombre y precio
            name_label = tk.Label(product_card, text=product['nombre'], font=("Helvetica", 14, "bold"))
            name_label.pack(pady=5)

            price_label = tk.Label(product_card, text=f"${product['precio']:.2f}", font=("Helvetica", 12), fg="red")
            price_label.pack(pady=5)

            # Descripción del producto
            desc_label = tk.Label(product_card, text=product['descripcion'], font=("Helvetica", 10), wraplength=200)
            desc_label.pack(pady=5)

    def open_add_window(self):
        """Abrir la ventana para agregar un nuevo producto"""
        add_window = ProductWindow(self.root, self)
        add_window.grab_set()

    def add_product(self, product):
        """Agregar un producto y actualizar la lista"""
        self.products.append(product)
        save_product(self.products)
        self.update_product_list()

def run_app():
    root = tk.Tk()
    app = CatalogApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
