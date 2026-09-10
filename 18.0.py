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

    def depositar(self, monto):
         if not self.activa:
            raise ValueError("Error: La cuenta no está activa.")
         if monto < 0:
            ValueError("Error: El monto a depositar debe ser positivo.")
         else:
            self.saldo += monto
            print(f"Se ha depositado ${monto:,.2f} al saldo.")

    def retirar(self, monto):
        if not self.activa:
            raise ValueError("Error: La cuenta no está activa.")
        if monto <= 0:
            raise ValueError("Error: El monto a retirar debe ser positivo.")
        if monto > self.saldo:
            raise ValueError(f"Error: Saldo insuficiente. Saldo disponible: ${self.saldo:,.2f}")
        self.saldo -= monto
        print(f"Se ha retirado ${monto:,.2f} de la cuenta.")

    def bloquear_cuenta(self):
        self.activa = False
        print("Se ha bloqueado la cuenta.")


class CuentaAhorro(CuentaBancaria):
    def __init__(self, numero_cuenta, titular, saldo_inicial=0.0, tasa_interes=0.05):
        super().__init__(numero_cuenta, titular, saldo_inicial)
        self.tasa_interes = tasa_interes

    def aplicar_interes(self):
        intereses = self.saldo * self.tasa_interes
        self.saldo += intereses
        print(f"Se ha aplicado un interés de ${intereses:,.2f} al saldo.")


class CuentaCorriente(CuentaBancaria):
    def __init__(self, numero_cuenta, titular, saldo_inicial=0.0, sobregiro=0.0):
        super().__init__(numero_cuenta, titular, saldo_inicial)
        self.sobregiro = sobregiro

    def retirar(self, monto):
        if not self.activa:
            raise ValueError("Error: La cuenta no está activa.")
        if monto <= 0:
            raise ValueError("Error: El monto a retirar debe ser positivo.")

        disponible = self.saldo + self.sobregiro
        if monto > disponible:
            raise ValueError(
                f"Error: Saldo insuficiente. Máximo disponible: ${disponible:,.2f}"
            )

        self.saldo -= monto
        print(f"Se ha retirado ${monto:,.2f} de la cuenta corriente.")


cuenta = CuentaBancaria("CTA-300", "Elena Vega", 500.0)
print("--- Ficha Inicial de Cuentas ---")
cuenta.mostrar_informacion()

print("--- Aplicando depósito a cuenta (+$300.00) ---")
cuenta.depositar(250.0)

try:
    print("--- Aplicando retiro a cuenta ($1000.00) ---")
    cuenta.retirar(1000.0)
except ValueError as error:
    print(error)

cuenta.bloquear_cuenta()

print("--- Aplicando retiro a cuenta ($50.00) ---")
try:
    cuenta.retirar(50.0)
except ValueError as error:
    print(error)

class CuentaAhorro(CuentaBancaria):

    def __init__(self, numero_cuenta, titular, saldo_inicial=0.0, tasa_interes=0.05):
        super().__init__(numero_cuenta, titular, saldo_inicial)
        self.tasa_interes = tasa_interes

    def aplicar_interes(self):
        intereses = self.saldo * self.tasa_interes
        self.saldo += intereses
        print(f"Se ha aplicado un interés de ${intereses:,.2f} al saldo.")


class CuentaCorriente(CuentaBancaria):

    def __init__(self, numero_cuenta, titular, saldo_inicial=0.0, sobregiro=300.0):
        super().__init__(numero_cuenta, titular, saldo_inicial)
        self.sobregiro = sobregiro

    def retirar(self, monto):
        if not self.activa:
            raise ValueError("Error: La cuenta no está activa.")
        if monto <= 0:
            raise ValueError("Error: El monto a retirar debe ser mayor a cero.")

        disponible = self.saldo + self.sobregiro
        if monto > disponible:
            raise ValueError(f"Error: Monto excede el límite permitido. Máximo disponible: ${disponible:,.2f}")

        self.saldo -= monto
        print(f"Se ha retirado ${monto:,.2f} de la cuenta corriente. Saldo: ${self.saldo:,.2f}")
        return self.saldo




print("=== PRUEBA CUENTA BASE ===")
cuenta = CuentaBancaria("CTA-300", "Elena Vega", 500.0)
cuenta.mostrar_informacion()
cuenta.depositar(250.0)

try:
    cuenta.retirar(1000.0)
except ValueError as error:
    print(error)

cuenta.bloquear_cuenta()

try:
    cuenta.retirar(50.0)
except ValueError as error:
    print(error)

print("\n=== PRUEBA CUENTA DE AHORRO ===")
ahorro = CuentaAhorro("CA-101", "Lucía Peña", 1000.0, 0.08)
ahorro.mostrar_informacion()
print("Aplicando intereses (8%)...")
ahorro.aplicar_interes()
ahorro.mostrar_informacion()

print("\n=== PRUEBA CUENTA CORRIENTE (SOBREGIRO) ===")
corriente = CuentaCorriente("CC-202", "Javier Rivas", 200.0, sobregiro=300.0)
corriente.mostrar_informacion()

print("Retirando $350.00 (usa saldo y $150 de sobregiro)...")
corriente.retirar(350.0)
corriente.mostrar_informacion()

print("Intentando retirar otros $200.00 (supera el límite)...")
try:
    corriente.retirar(200.0)
except ValueError as error:
    print(error)