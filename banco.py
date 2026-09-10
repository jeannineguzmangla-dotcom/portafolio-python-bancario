from cuentas import CuentaBancaria, CuentaAhorro, CuentaCorriente

class Banco:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cuentas = {
            "CTA-100": CuentaBancaria("CTA-100", "Elena Vega", 500.0),
            "CA-200": CuentaAhorro("CA-200", "Lucía Peña", 1000.0, tasa_interes=0.04),
            "CC-300": CuentaCorriente("CC-300", "Javier Rivas", 200.0, sobregiro=500.0)
        }

    def registrar_cuenta(self, cuenta):
        if cuenta.numero_cuenta in self.cuentas:
            raise ValueError(f"Error: Ya existe una cuenta con el número '{cuenta.numero_cuenta}'.")
        self.cuentas[cuenta.numero_cuenta] = cuenta
        print(f"Cuenta {cuenta.numero_cuenta} registrada exitosamente.")

    def obtener_cuenta(self, numero_cuenta):
        if numero_cuenta not in self.cuentas:
            raise ValueError(f"Error: La cuenta '{numero_cuenta}' no existe.")
        return self.cuentas[numero_cuenta]

    def transferir(self, origen_num, destino_num, monto):
        if origen_num == destino_num:
            raise ValueError("Error: No se puede transferir a la misma cuenta.")
        
        origen = self.obtener_cuenta(origen_num)
        destino = self.obtener_cuenta(destino_num)

        origen.retirar(monto)
        destino.depositar(monto)
        print(f"Transferencia de ${monto:,.2f} completada exitosamente.")

    def ejecutar_cierre_global(self):
        print(f"\n--- Ejecutando Cierre Global en {self.nombre} ---")
        for cuenta in self.cuentas.values():
            cuenta.cierre_mensual()

    def listar_cuentas(self):
        print("\n" + "=" * 65)
        print(f"              CATÁLOGO DE CUENTAS - {self.nombre.upper()}")
        print("=" * 65)
        for cuenta in self.cuentas.values():
            print(cuenta)
        print("=" * 65)