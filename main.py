from cuentas import CuentaBancaria, CuentaAhorro, CuentaCorriente
from banco import Banco

def ejecutar_sistema():
    mi_banco = Banco("Banco Central")

    while True:
        print("\n" + "=" * 45)
        print("         SISTEMA BANCARIO MODULAR        ")
        print("=" * 45)
        print("1. Registrar nueva cuenta")
        print("2. Listar todas las cuentas")
        print("3. Depositar fondos")
        print("4. Retirar fondos")
        print("5. Realizar transferencia")
        print("6. Ejecutar cierre de mes global")
        print("7. Salir")

        try:
            opcion = int(input("Seleccione una opción: "))

            if opcion == 1:
                print("\nTipo de cuenta: 1: Estándar | 2: Ahorro | 3: Corriente")
                tipo = input("Seleccione el tipo (1/2/3): ").strip()
                num = input("Número de cuenta (ej. CTA-500): ").strip()
                titular = input("Nombre del titular: ").strip()
                saldo = float(input("Saldo inicial: "))

                if tipo == "1":
                    nueva_cuenta = CuentaBancaria(num, titular, saldo)
                elif tipo == "2":
                    nueva_cuenta = CuentaAhorro(num, titular, saldo)
                elif tipo == "3":
                    nueva_cuenta = CuentaCorriente(num, titular, saldo)
                else:
                    print("Error: Tipo de cuenta no válido.")
                    continue

                mi_banco.registrar_cuenta(nueva_cuenta)

            elif opcion == 2:
                mi_banco.listar_cuentas()

            elif opcion == 3:
                num = input("Número de cuenta: ").strip()
                monto = float(input("Monto a depositar: "))
                mi_banco.obtener_cuenta(num).depositar(monto)

            elif opcion == 4:
                num = input("Número de cuenta: ").strip()
                monto = float(input("Monto a retirar: "))
                mi_banco.obtener_cuenta(num).retirar(monto)

            elif opcion == 5:
                origen = input("Cuenta de origen: ").strip()
                destino = input("Cuenta de destino: ").strip()
                monto = float(input("Monto a transferir: "))
                mi_banco.transferir(origen, destino, monto)

            elif opcion == 6:
                mi_banco.ejecutar_cierre_global()

            elif opcion == 7:
                print("Cerrando sesión del sistema bancario. Hasta luego.")
                break

            else:
                print("Opción inválida. Ingrese un valor entre 1 y 7.")

        except ValueError as e:
            print(f"\nOperación rechazada: {e}")

if __name__ == "__main__":
    ejecutar_sistema()