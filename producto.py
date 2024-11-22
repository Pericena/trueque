import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import json


# Utilidades para cargar y guardar productos
def load_products():
    try:
        with open("products.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_products(products):
    with open("products.json", "w") as f:
        json.dump(products, f, indent=4)

class ProductWindow(tk.Toplevel):
    def __init__(self, parent, catalog_app, product=None, idx=None):
        super().__init__(parent)
        self.catalog_app = catalog_app
        self.product = product
        self.idx = idx
        self.title("Editar Producto" if product else "Agregar Producto")
        self.geometry("400x500")

        # Campos de entrada
        tk.Label(self, text="Nombre:", font=("Helvetica", 12)).pack(pady=5)
        self.name_entry = tk.Entry(self, font=("Helvetica", 12))
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, product["nombre"] if product else "")

        tk.Label(self, text="Descripción:", font=("Helvetica", 12)).pack(pady=5)
        self.desc_entry = tk.Entry(self, font=("Helvetica", 12))
        self.desc_entry.pack(pady=5)
        self.desc_entry.insert(0, product["descripcion"] if product else "")

        tk.Label(self, text="Precio:", font=("Helvetica", 12)).pack(pady=5)
        self.price_entry = tk.Entry(self, font=("Helvetica", 12))
        self.price_entry.pack(pady=5)
        self.price_entry.insert(0, product["precio"] if product else "")

        tk.Label(self, text="URL de Imagen:", font=("Helvetica", 12)).pack(pady=5)
        self.image_url_entry = tk.Entry(self, font=("Helvetica", 12))
        self.image_url_entry.pack(pady=5)
        self.image_url_entry.insert(0, product["imagen_url"] if product else "")

        # Botón
        desc_label = tk.Label(
            product_card,
            text=product["descripcion"],
            font=("Helvetica", 10),
            wraplength=180,
            )
        desc_label.pack(pady=5)

        # Vista previa de la imagen
        self.image_preview_label = tk.Label(self, text="Vista previa", font=("Helvetica", 10, "italic"))
        self.image_preview_label.pack(pady=10)
        self.image_preview_canvas = tk.Label(self)
        self.image_preview_canvas.pack(pady=5)

        self.image_url_entry.bind("<KeyRelease>", self.update_image_preview)

        tk.Button(
            self, 
            text="Guardar", 
            command=self.save_product, 
            bg="#4CAF50", 
            fg="white", 
            font=("Helvetica", 12)
        ).pack(pady=20)

    def update_image_preview(self, event=None):
        image_url = self.image_url_entry.get()
        if image_url:
            try:
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                img.thumbnail((100, 100))
                img_tk = ImageTk.PhotoImage(img)
                self.image_preview_canvas.config(image=img_tk)
                self.image_preview_canvas.image = img_tk
            except Exception as e:
                self.image_preview_canvas.config(image="")
                messagebox.showwarning("Error", "No se pudo cargar la imagen.")

    def save_product(self):
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
            "nombre": name,
            "descripcion": description,
            "precio": price,
            "imagen_url": image_url
        }

        if self.product and self.idx is not None:
            self.catalog_app.update_product(self.idx, new_product)
        else:
            self.catalog_app.add_product(new_product)

        self.destroy()

class CatalogApp: #Representa toda la pantalla con los productos
    def __init__(self, root):
        self.root = root
        self.root.title("Catálogo de Productos")
        self.root.geometry("900x700")
        self.products = load_products()

        # Header(Encabezado)
        header_frame = tk.Frame(self.root, bg="#4CAF50", height=50)
        header_frame.pack(fill=tk.X)

        tk.Label(header_frame, text="Catálogo de Productos", bg="#4CAF50", fg="white", font=("Helvetica", 18, "bold")).pack(side=tk.LEFT, padx=10)
        for action in ["Agregar", "Actualizar"]:
            tk.Button(header_frame, text=action, command=self.open_add_window, bg="white", font=("Helvetica", 12)).pack(side=tk.RIGHT, padx=5)

        # Contenedor principal (Catalogo de productos)
        self.products_frame = tk.Frame(self.root)
        self.products_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.update_product_list()

    def update_product_list(self):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        for idx, product in enumerate(self.products):
            card = tk.Frame(self.products_frame, relief=tk.RIDGE, borderwidth=2, width=250, height=350)
            card.grid(row=idx // 3, column=idx % 3, padx=10, pady=10)
            card.grid_propagate(False)

            # Imagen
            image_label = tk.Label(card)
            image_label.pack(pady=10)

            if "imagen_url" in product:
                try:
                    response = requests.get(product["imagen_url"])
                    img = Image.open(BytesIO(response.content))
                    img.thumbnail((150, 150))
                    img_tk = ImageTk.PhotoImage(img)
                    image_label.config(image=img_tk)
                    image_label.image = img_tk
                except Exception:
                    image_label.config(text="Imagen no disponible")

            # Nombre y precio
            tk.Label(card, text=product["nombre"], font=("Helvetica", 14, "bold")).pack(pady=5)
            tk.Label(card, text=f"${product['precio']:.2f}", font=("Helvetica", 12), fg="red").pack(pady=5)

            # Botones
            tk.Button(card, text="Editar", command=lambda idx=idx: self.edit_product(idx), bg="#FFC107", fg="black").pack(side=tk.LEFT, padx=5, pady=5)
            tk.Button(card, text="Eliminar", command=lambda idx=idx: self.delete_product(idx), bg="red", fg="white").pack(side=tk.RIGHT, padx=5, pady=5)

    def edit_product(self, idx):
        product = self.products[idx]
        ProductWindow(self.root, self, product=product, idx=idx)

    def delete_product(self, idx):
        if messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este producto?"):
            self.products.pop(idx)
            save_products(self.products)
            self.update_product_list()

    def open_add_window(self):
        ProductWindow(self.root, self)

    def add_product(self, product):
        self.products.append(product)
        save_products(self.products)
        self.update_product_list()

    def update_product(self, idx, product):
        self.products[idx] = product
        save_products(self.products)
        self.update_product_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = CatalogApp(root)
    root.mainloop()
