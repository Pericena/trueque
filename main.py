import tkinter as tk
from tkinter import messagebox
import json
from producto import ProductWindow
from utils import load_products, save_product
from PIL import Image, ImageTk
import requests
import customtkinter as ctk
from io import BytesIO


class CatalogApp: #Home
    def __init__(self, root):
        self.root = root
        self.root.title("Catálogo de Productos")
        self.root.geometry("1270x780")

        # Productos
        self.products = load_products()

        # Cabecera con botones de acción
        #Tamaño de la cabecera
        self.header_frame = tk.Frame(root, bg="lightgray", height=50)
        self.header_frame.pack(fill="x", pady=5)

        #Botón de Logo
        self.add_button = tk.Button(
            self.header_frame, text="Logo", command=self.open_add_window, width=10
        )
        self.add_button.pack(side="left", padx=5)

        #Botón del Buscador
        self.update_button = tk.Button(
            self.header_frame, text="Buscador", command=self.update_product_list, width=10
        )
        self.update_button.pack(side="left", padx=5)
        
        #Botón de Promociones
        self.add_button = tk.Button(
            self.header_frame, text="Promociones", command=self.open_add_window, width=10
        )
        self.add_button.pack(side="left", padx=5)

        #Botón de Agregar
        self.update_button = tk.Button(
            self.header_frame, text="Agregar", command=self.update_product_list, width=10
        )
        self.update_button.pack(side="left", padx=5)

        #Botón de Usuario
        self.add_button = tk.Button(
            self.header_frame, text="Usuario", command=self.open_add_window, width=10
        )
        self.add_button.pack(side="left", padx=5)


        # Marco para los productos
        self.products_frame = tk.Frame(root)
        self.products_frame.pack(pady=10, expand=True, fill="both")

        self.update_product_list()

    def update_product_list(self):
        """Actualizar la visualización de productos en estilo "card"."""        
        for widget in self.products_frame.winfo_children():
            widget.destroy()  # Limpiar el marco de productos

        for index, product in enumerate(self.products):
            product_card = tk.Frame(
                self.products_frame,
                relief="solid",
                borderwidth=2,
                width=200,
                height=300,
            )
            product_card.grid_propagate(False)
            product_card.grid(row=index // 3, column=index % 3, padx=10, pady=10)

            # Imagen del producto
            image_label = tk.Label(product_card)
            image_label.pack(pady=5)

            if "imagen_url" in product:
                try:
                    response = requests.get(product['imagen_url'], timeout=5)
                    img = Image.open(BytesIO(response.content))
                    img.thumbnail((150, 150))
                    img_tk = ImageTk.PhotoImage(img)
                    image_label.config(image=img_tk)
                    image_label.image = img_tk
                except Exception:
                    image_label.config(text="Imagen no disponible")

            # Nombre
            name_label = tk.Label(
                product_card, text=product["nombre"], font=("Helvetica", 14, "bold")
            )
            name_label.pack(pady=5)

            # Precio
            price_label = tk.Label(
                product_card,
                text=f"TRC {product['precio']:.2f}",
                font=("Helvetica", 12),
                fg="red",
            )
            price_label.pack(pady=5)


    def open_add_window(self):
        """Abrir ventana para agregar un nuevo producto"""
        add_window = ProductWindow(self.root, self)
        add_window.grab_set()

    def add_product(self, product):
        """Agregar producto y actualizar lista"""
        self.products.append(product)
        save_product(self.products)
        self.update_product_list()


def run_app():
    root = tk.Tk()
    app = CatalogApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
