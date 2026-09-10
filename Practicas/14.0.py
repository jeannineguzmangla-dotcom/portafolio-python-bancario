import json

def guardar_cartera(datos):
    with open("cartera.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
        print("Cartera guardada con éxito.")
def cargar_cartera():
    try:
        with open("cartera.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            return datos
    except FileNotFoundError:
        print("Aviso: No se encontró ninguna cartera en el disco.")
        return {
    "CLI01": {"nombre": "Laura Peña", "servicios": ["Banca Móvil", "Seguro"], "credito_aprobado": 5000.0},
    "CLI02": {"nombre": "Roberto Gil", "servicios": ["Tarjeta Oro"], "credito_aprobado": 2500.0}
}

def agregar_servicio(id_cliente, nuevo_servicio):
    cartera = cargar_cartera()
    if id_cliente == "CLI01":
        cartera["CLI01"]["servicios"].append(nuevo_servicio)
        guardar_cartera(cartera)
        print(f"Servicio '{nuevo_servicio}' agregado con éxito.")
        
    else:
        print("Error: El cliente no existe en la cartera.")

def mostrar_cartera():
    cartera = cargar_cartera()
    print("\n" + "=" * 40)
    print("           CARTERA DE CLIENTES")
    print("=" * 40)
    for id_cliente, datos in cartera.items():
        print(f"ID: {id_cliente:<3} | Nombre: {datos['nombre']}")
        print(f"Servicio contractado: [{', '.join(datos['servicios'])}]")
        print(f"Credito aprobado: ${datos['credito_aprobado']:,.2f}")
        print("-" * 40)
    print("=" * 40 + "\n")

while True:
    print("Bienvenido al sistema de gestión de clientes.")
    print("Utilice las siguientes opciones:")
    print("1. Ver cartera completa")
    print("2. Agregar servicio a cliente existente")
    print("3. Registrar nuevo cliente (ID, Nombre, Crédito inicial)")
    print("4. Salir")

    try:
        opcion = int(input("Elija una opción: "))
    except ValueError:
        print("Error: Por favor ingrese un número del menú.\n")
        continue
    
    if opcion == 1:
        mostrar_cartera()
    
    elif opcion == 2:
        try:
            id_cliente = input("Ingrese el ID del cliente: ").strip()
            servicio = input("Ingrese el servicio a agregar: ").strip()
            agregar_servicio(id_cliente, servicio)
        except ValueError:
            print("Error: Ingrese valores numéricos válidos en ID y servicio.\n")
            
    elif opcion == 3:
        try:
            id_cliente = input("Ingrese el ID del cliente: ").strip()
            nombre = input("Ingrese el nombre del cliente: ").strip()
            credito = float(input("Ingrese el crédito inicial: "))
            if credito <= 0:
                print("Error: El crédito debe ser mayor a 0.\n")
                continue
            
            datos = {"nombre": nombre, "servicios": [], "credito_aprobado": credito}
            cartera = cargar_cartera()
            cartera[id_cliente] = datos
            guardar_cartera(cartera)
            print(f"Cliente '{nombre}' agregado con éxito.")
        except ValueError:
            print("Error: Ingrese valores numéricos válidos en ID, nombre y crédito.\n")
            
    elif opcion == 4:
        print("Gracias por usar el sistema. Hasta luego.")
        break
    
    else:
        print("Opción no válida. Intente nuevamente.\n")
    