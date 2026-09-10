class CuentaBancaria:

    def __init__(self, numero_cuenta, titular, saldo_inicial=0.0):
        self.numero_cuenta = numero_cuenta
        self.titular = titular
        
        
        if saldo_inicial < 0:
            self.saldo = 0.0
            print("Error: El saldo inicial debe ser positivo.")
        else:
            self.saldo = saldo_inicial
        self.activa= True

    
            

    def mostrar_informacion(self):
        estado = "Activa" if self.activa else "Bloqueada"
        print(f"Número de cuenta: {self.numero_cuenta}")
        print(f"Titular:          {self.titular}")
        print(f"Saldo actual:     ${self.saldo:,.2f}")
        print(f"Estado:           {estado}")
        print("-" * 40)

cuenta_1= CuentaBancaria("CTA-100", "Valeria Silva", 1500.0)
cuenta_2= CuentaBancaria("CTA-200", "Martín Castro", 800.0)

print("--- Ficha Inicial de Cuentas ---")
cuenta_1.mostrar_informacion()
cuenta_2.mostrar_informacion()

print("--- Aplicando depósito a cuenta_2 (+$300.00) ---")
cuenta_2.saldo += 300.0

print("--- Ficha Actual de Cuentas ---")
cuenta_1.mostrar_informacion()
cuenta_2.mostrar_informacion()




   