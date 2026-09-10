producto = {
    "nombre": "Teclado Mecánico",
    "precio": 85.0,
    "stock": 10,
    "categoria": "Electrónica"
}

producto["stock"] += 5
garantia=producto.get("garantia", "No disponible")
print(f"Nombre del producto: {producto['nombre']}, Precio: ${producto['precio']}, Stock: {producto['stock']}, Garantía: {garantia}")

    

        
        
            



