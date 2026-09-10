#Sistema Integral de Finanzas: Persistencia JSON y Auditoría CSV

import json
import csv

def cargar_cuentas():
    try:
        with open('cuentas.json') as f:
            cuentas = json.load(f)
            return cuentas
    except FileNotFoundError:
        print("Error: No se encontró ninguna cuenta en el disco.")
        return {"CTA-100": {"titular": "Valeria Silva", "saldo": 1500.0},
            "CTA-200": {"titular": "Martín Castro", "saldo": 800.0}}

def guardar_cuentas(cuentas):
    with open('cuentas.json', 'w') as f:
        json.dump(cuentas, f, indent=4, ensure_ascii=False)
        print("Cuentas guardadas con éxito.")

def registar_en_log(origen, destino, monto, estado):
    with open("auditoria.csv", "a", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow([origen, destino, monto, estado])
        print(f"Transacción registrada con éxito.")

def ejecutar_tranferencia(origen, destino, monto):
    try:
        cuentas = cargar_cuentas()
        if origen in cuentas and destino in cuentas:
            cuentas[origen]["saldo"] -= monto
            cuentas[destino]["saldo"] += monto
            if origen == "CTA-100" and destino == "CTA-100":
                print("Error: No se puede transferir dinero a sí mismo.")
            else:
                monto > 0 and registar_en_log(origen, destino, monto, "Saldo positivo")
                monto < 0 and registar_en_log(origen, destino, monto, "Saldo negativo")
        if origen not in cuentas:
            print("Rechazo: Origen no existe.")
        elif destino not in cuentas:
            print("Rechazo: Destino no existe.")
        else:
            guardar_cuentas(cuentas)
    except ValueError:
        print("Error: Ingrese valores numéricos válidos en origen, destino y monto.")
    finally:
        print("Transacción ejecutada con éxito.")

while True:
    try:
        print("Bienvenido al sistema de gestión de cuentas.")
        print("Utilice las siguientes opciones:")
        print("1. Ver cuentas")
        print("2. Registrar transacción")
        print("3. Ver auditoría")
        print("4. Salir")

        opcion = int(input("Elija una opción: "))
    except ValueError:
        print("Error: Por favor ingrese un número del menú.\n")
        continue

    if opcion == 1:
        cuentas = cargar_cuentas()
        print("\n" + "=" * 40)
        print("           CUENTAS")
        print("=" * 40)
        for id_cuenta, datos in cuentas.items():
            print(f"ID: {id_cuenta:<3} | Titular: {datos['titular']}")
            print(f"Saldo: ${datos['saldo']:,.2f}")
            print("-" * 40)
        print("=" * 40 + "\n")

        
    elif opcion == 2:
        try:
            origen = input("Ingrese el ID de la cuenta de origen: ").strip()
            destino = input("Ingrese el ID de la cuenta de destino: ").strip()
            monto = float(input("Ingrese el monto a transferir: "))
            ejecutar_tranferencia(origen, destino, monto)
        except ValueError:
            print("Error: Ingrese valores numéricos válidos en origen, destino y monto.\n")

    elif opcion == 3:
        with open("auditoria.csv", "r", encoding="utf-8") as archivo:
            print("\n" + "=" * 40)
            print("           AUDITORIA")
            print("=" * 40)
            for linea in csv.reader(archivo):
                print(f"Origen: {linea[0]}, Destino: {linea[1]}, Monto: {linea[2]}, Estado: {linea[3]}")
            print("=" * 40 + "\n")

    elif opcion == 4:
        print("Gracias por usar el sistema. Hasta luego.")
        break
    
    else:
        print("Opción no válida. Intente nuevamente.\n")
        
            
    


    