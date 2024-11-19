import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Para manejar imágenes
import requests  # Para descargar imágenes desde URLs
import json

# Función para cargar los productos desde el archivo JSON
def cargar_productos():
    try:
        with open("productos.json", "r") as archivo:
            productos = json.load(archivo)
    except FileNotFoundError:
        productos = []
    return productos

# Función para cargar el carrito desde el archivo JSON
def cargar_carrito():
    try:
        with open("lista_producto.json", "r") as archivo:
            carrito = json.load(archivo)
    except FileNotFoundError:
        carrito = []
    return carrito

# Función para guardar los productos en el archivo JSON
def guardar_productos(productos):
    with open("productos.json", "w") as archivo:
        json.dump(productos, archivo, indent=4)

# Función para guardar el carrito en el archivo JSON
def guardar_carrito(carrito):
    with open("lista_producto.json", "w") as archivo:
        json.dump(carrito, archivo, indent=4)

# Función para publicar un producto nuevo
def publicar_producto():
    id_producto = len(productos) + 1  # Genera un ID único para el nuevo producto
    nombre = entry_nombre.get()
    descripcion = entry_descripcion.get()
    id_usuario = entry_usuario.get()
    estado = entry_estado.get()
    precio = float(entry_precio.get())
    imagen_url = entry_imagen.get()
    
    nuevo_producto = {
        "id_producto": id_producto,
        "nombre": nombre,
        "descripcion": descripcion,
        "id_usuario": int(id_usuario),
        "estado": estado,
        "precio": precio,
        "imagen_url": imagen_url
    }
    
    productos.append(nuevo_producto)
    guardar_productos(productos)
    messagebox.showinfo("Producto Publicado", f"Producto '{nombre}' publicado con éxito.")
    listar_productos()

# Función para listar todos los productos
def listar_productos():
    lista_productos.delete(0, tk.END)
    for producto in productos:
        lista_productos.insert(tk.END, f"{producto['id_producto']} - {producto['nombre']} - ${producto['precio']} - {producto['estado']}")

# Función para mostrar la imagen seleccionada
def mostrar_imagen():
    seleccion = lista_productos.curselection()
    if seleccion:
        index = seleccion[0]
        producto = productos[index]
        url_imagen = producto.get("imagen_url", "")
        
        if url_imagen:
            try:
                # Descargar y mostrar la imagen
                response = requests.get(url_imagen, stream=True)
                response.raise_for_status()
                imagen = Image.open(response.raw)
                imagen = imagen.resize((200, 200))  # Redimensionar para ajustar al frame
                imagen_tk = ImageTk.PhotoImage(imagen)
                etiqueta_imagen.config(image=imagen_tk)
                etiqueta_imagen.image = imagen_tk  # Guardar referencia para evitar que sea recolectado por el GC
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")
        else:
            messagebox.showwarning("Advertencia", "Este producto no tiene URL de imagen.")
    else:
        messagebox.showerror("Error", "Seleccione un producto para ver la imagen.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Marketplace Básico")
ventana.geometry("1200x600")

# Cargar productos y carrito desde JSON
productos = cargar_productos()
carrito = cargar_carrito()

# Crear un frame principal para dividir el contenido
frame_productos = tk.Frame(ventana)
frame_productos.pack(side=tk.LEFT, padx=20, pady=20)

frame_carrito = tk.Frame(ventana)
frame_carrito.pack(side=tk.RIGHT, padx=20, pady=20)

frame_imagen = tk.Frame(ventana)
frame_imagen.pack(side=tk.BOTTOM, pady=20)

# Widgets en el frame_productos
tk.Label(frame_productos, text="Nombre Producto").grid(row=0, column=0, pady=5, sticky="e")
entry_nombre = tk.Entry(frame_productos)
entry_nombre.grid(row=0, column=1, pady=5)

tk.Label(frame_productos, text="Descripción Producto").grid(row=1, column=0, pady=5, sticky="e")
entry_descripcion = tk.Entry(frame_productos)
entry_descripcion.grid(row=1, column=1, pady=5)

tk.Label(frame_productos, text="ID Usuario").grid(row=2, column=0, pady=5, sticky="e")
entry_usuario = tk.Entry(frame_productos)
entry_usuario.grid(row=2, column=1, pady=5)

tk.Label(frame_productos, text="Estado (disponible, en trueque)").grid(row=3, column=0, pady=5, sticky="e")
entry_estado = tk.Entry(frame_productos)
entry_estado.grid(row=3, column=1, pady=5)

tk.Label(frame_productos, text="Precio Producto").grid(row=4, column=0, pady=5, sticky="e")
entry_precio = tk.Entry(frame_productos)
entry_precio.grid(row=4, column=1, pady=5)

tk.Label(frame_productos, text="URL Imagen").grid(row=5, column=0, pady=5, sticky="e")
entry_imagen = tk.Entry(frame_productos)
entry_imagen.grid(row=5, column=1, pady=5)

tk.Button(frame_productos, text="Publicar Producto", command=publicar_producto).grid(row=6, column=0, columnspan=2, pady=5)

lista_productos = tk.Listbox(frame_productos, width=50, height=20)
lista_productos.grid(row=7, column=0, columnspan=2, pady=10)

tk.Button(frame_productos, text="Mostrar Imagen", command=mostrar_imagen).grid(row=8, column=0, columnspan=2, pady=5)

# Frame para mostrar la imagen
etiqueta_imagen = tk.Label(frame_imagen, text="Imagen del Producto")
etiqueta_imagen.pack()

# Mostrar los productos al inicio
listar_productos()

# Iniciar la interfaz
ventana.mainloop()
