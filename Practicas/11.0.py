def registrar_movimientos(descripcion, monto):
    registro = f"MOVIMIENTO: {descripcion} | MONTO: ${monto:,.2f}\n"
    with open("historial.txt", "a") as f:
        f.write(registro)
    print("Registro Guardado con éxito.")

def ver_historial():
    try:
        with open("historial.txt", "r") as f:
            contenido = f.read()
            if contenido:
                print(contenido)
            else:
                print("Aviso: No se encontró ningún historial previo en el disco.")
    except FileNotFoundError:
        print("Aviso: No se encontró ningún historial previo en el disco.")


while True:
    print("Bienvenido al sistema de gestión de cuentas bancarias.")
    print("Utilice las siguientes opciones:")
    print("1. Registrar nuevo movimiento")
    print("2. Ver historial")
    print("3. Salir")

    opcion = int(input("Elija una opción: "))

    if opcion == 1:
        try:
            descripcion = input("Ingrese la descripción del movimiento: ")
            monto = float(input("Ingrese el monto del movimiento: "))
            registrar_movimientos(descripcion, monto)
        except ValueError as e:
            print(f"Error, Ingrese un monto valido, no letras: {e}")
    elif opcion == 2:
        ver_historial()
    elif opcion == 3:
        print("Adiós.")
        break
    else:
        print("Opción no válida. Intente nuevamente.")
