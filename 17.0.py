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
        

    def bloquear_cuenta(self):
        self.activa = False
        print("Se ha bloqueado la cuenta.")

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
