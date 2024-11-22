import json

def load_products():
    """Cargar productos desde un archivo JSON"""
    try:
        with open("productos.json", "r") as file:
            products = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        products = []
    return products

def save_product(products):
    """Guardar productos en el archivo JSON"""
    with open("productos.json", "w") as file:
        json.dump(products, file, indent=4)
