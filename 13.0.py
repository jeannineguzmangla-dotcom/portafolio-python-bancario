import csv

def inicializar_catalogo():
    with open("catalogo.csv", "w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["ID", "Descripcion", "Precio unitario", "Stock disponible"])
        writer.writerow(["1", "Pantalon Azul", "10.00", "10"])
        writer.writerow(["2", "Camisa", "15.00", "5"])
        writer.writerow(["3", "Monitor, LED 24 pulgadas", "120.00", "10"])
    print("Catálogo inicializado con éxito en 'catalogo.csv'.\n")


def agregar_producto(id_prod, descripcion, precio, stock):
    with open("catalogo.csv", "a", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow([id_prod, descripcion, f"{precio:.2f}", stock])
    print(f"Producto '{descripcion}' agregado con éxito.\n")


def mostrar_reporte():
    try:
        with open("catalogo.csv", "r", newline="", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            next(lector, None)  # Salta la fila de encabezado

            total_inventario = 0.0

            print("\n" + "=" * 65)
            print("                REPORTE DE INVENTARIO COMERCIAL")
            print("=" * 65)

            for row in lector:
                if not row:
                    continue
                id_prod, descripcion, precio_str, stock_str = row
                precio = float(precio_str)
                stock = int(stock_str)
                subtotal = precio * stock
                total_inventario += subtotal

                print(f"ID {id_prod:<3} | {descripcion:<25} | ${precio:>7.2f} x {stock:>3} | Subtotal: ${subtotal:>8.2f}")

            print("-" * 65)
            print(f"VALOR TOTAL DEL INVENTARIO: ${total_inventario:,.2f}")
            print("=" * 65 + "\n")

    except FileNotFoundError:
        print("Error: El catálogo aún no existe. Debe crearlo con la opción 1.\n")


while True:
    print("Bienvenido al sistema de gestión de inventario.")
    print("Utilice las siguientes opciones:")
    print("1. Inicializar catálogo")
    print("2. Agregar producto")
    print("3. Mostrar reporte")
    print("4. Salir")

    try:
        opcion = int(input("Elija una opción: "))
    except ValueError:
        print("Error: Por favor ingrese un número del menú.\n")
        continue

    if opcion == 1:
        inicializar_catalogo()

    elif opcion == 2:
        try:
            id_prod = input("Ingrese el ID del producto: ").strip()
            descripcion = input("Ingrese la descripción del producto: ").strip()
            precio = float(input("Ingrese el precio unitario del producto: "))
            stock = int(input("Ingrese el stock disponible del producto: "))

            if precio <= 0 or stock < 0:
                print("Error: El precio y stock deben ser mayores a 0.\n")
                continue

            agregar_producto(id_prod, descripcion, precio, stock)
        except ValueError:
            print("Error: Ingrese valores numéricos válidos en precio y stock.\n")

    elif opcion == 3:
        mostrar_reporte()

    elif opcion == 4:
        print("Gracias por usar el sistema. Hasta luego.")
        break

    else:
        print("Opción no válida. Intente nuevamente.\n")