def crear_transacciones_muestra():
    with open("transacciones.txt", "w", encoding="utf-8") as archivo:
        archivo.write(
            "Nombre,Monto,Tipo\n"
            "Salario,1500.00,ingreso\n"
            "Supermercado,85.50,egreso\n"
            "Venta Monitor,120.00,ingreso\n"
            "Servicios,45.00,egreso\n"
            "Mantenimiento,60.00,egreso\n"
        )
    print("Archivo 'transacciones.txt' creado con transacciones de muestra.")


def analizar_balance():
    try:
        with open("transacciones.txt", "r", encoding="utf-8") as f:
            total_ingresos = 0.0
            total_egresos = 0.0

            # 1. Saltar la línea de cabecera (Nombre,Monto,Tipo)
            next(f, None)

            # 2. Procesar registro por registro
            for linea in f:
                
                linea = linea.strip()
                if not linea:  # Salta líneas vacías si las hubiera
                    continue

                campos = [c.strip() for c in linea.split(",")]
                if len(campos) != 3:
                    continue

                nombre, monto_str, tipo = campos
                monto = float(monto_str)

                if tipo.lower() == "ingreso":
                    total_ingresos += monto
                elif tipo.lower() == "egreso":
                    total_egresos += monto

            # 3. Reporte final fuera del bucle
            balance = total_ingresos - total_egresos
            print("\n" + "=" * 40)
            print("           BALANCE GENERAL              ")
            print("=" * 40)
            print(f"Total ingresos:  ${total_ingresos:,.2f}")
            print(f"Total egresos:   ${total_egresos:,.2f}")
            print("-" * 40)
            print(f"Balance neto:    ${balance:,.2f}")
            print("=" * 40 + "\n")

    except FileNotFoundError:
        print("Aviso: No se encontró ningún archivo 'transacciones.txt' en el disco.\n")


# Flujo principal
while True:
    print("Bienvenido al sistema de gestión de transacciones.")
    print("1. Restablecer archivo con datos de muestra")
    print("2. Registrar una nueva transacción")
    print("3. Analizar balance general")
    print("4. Salir")

    try:
        opcion = int(input("Elija una opción: "))
    except ValueError:
        print("Error: Por favor, ingrese un número del menú.\n")
        continue

    if opcion == 1:
        crear_transacciones_muestra()

    elif opcion == 2:
        nombre = input("Ingrese el concepto/destinatario: ").strip()
        try:
            monto = float(input("Ingrese el monto: "))
            tipo = input("Tipo (ingreso / egreso): ").strip().lower()
            if tipo not in ["ingreso", "egreso"]:
                print("Error: El tipo debe ser 'ingreso' o 'egreso'.\n")
                continue

            with open("transacciones.txt", "a", encoding="utf-8") as archivo:
                archivo.write(f"{nombre},{monto:.2f},{tipo}\n")
            print("Transacción registrada con éxito.\n")
        except ValueError:
            print("Error: El monto debe ser numérico.\n")

    elif opcion == 3:
        analizar_balance()

    elif opcion == 4:
        print("Gracias por usar el sistema. Hasta luego.")
        break

    else:
        print("Opción no válida. Intente nuevamente.\n")

    
