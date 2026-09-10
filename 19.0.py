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
    
        
                
    
    def __str__(self):
        return f"[{self.numero_cuenta}] Titular: {self.titular:<15} | Saldo: ${self.saldo:>10,.2f}"
    
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

    def cierre_mensual(self):
            comision = 5.0
            if self.saldo >= comision:
                self.saldo -= comision
                print(f"[{self.numero_cuenta}] Mantenimiento mensual descontado: -${comision:,.2f}")
            else:
                print(f"[{self.numero_cuenta}] Saldo insuficiente para deducir comisión de mantenimiento.")


class CuentaAhorro(CuentaBancaria):
    def __init__(self, numero_cuenta, titular, saldo_inicial=0.0, tasa_interes=0.05):
        super().__init__(numero_cuenta, titular, saldo_inicial)
        self.tasa_interes = tasa_interes

    def __str__(self):
        return f"[Ahorro] {self.numero_cuenta} - {self.titular} | Saldo: ${self.saldo:,.2f} | Tasa: {self.tasa_interes * 100:.1f}%"
    def aplicar_interes(self):
        intereses = self.saldo * self.tasa_interes
        self.saldo += intereses
        print(f"[{self.numero_cuenta}] Interés abonado (+{self.tasa_interes * 100:.1f}%): +${intereses:,.2f}")
    def cierre_mensual(self):
        self.aplicar_interes()

class CuentaCorriente(CuentaBancaria):
    def __init__(self, numero_cuenta, titular, saldo_inicial=0.0, sobregiro=0.0):
        super().__init__(numero_cuenta, titular, saldo_inicial)
        self.sobregiro = sobregiro
    def __str__(self):
        return f"[Corriente] [{self.numero_cuenta}] Titular: {self.titular:<15} | Saldo: ${self.saldo:>10,.2f} | Sobregiro: ${self.sobregiro:,.2f}"

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

    def cierre_mensual(self):
        comision = 5.0
        if self.saldo >= comision:
            self.saldo -= comision
            print(f"[{self.numero_cuenta}] Mantenimiento mensual descontado: -${comision:,.2f}")
        else:
            print(f"[{self.numero_cuenta}] Saldo insuficiente para deducir comisión de mantenimiento.")

cuenta_estandar = CuentaBancaria("CTA-100", "Elena Vega", 500.0)
cuenta_ahorro = CuentaAhorro("CA-200", "Lucía Peña", 1000.0, tasa_interes=0.08)
cuenta_corriente = CuentaCorriente("CC-300", "Javier Rivas", 200.0, sobregiro=300.0)
cuenta_corriente.retirar(350.0)

banco = [cuenta_estandar, cuenta_ahorro, cuenta_corriente]

print("\n" + "=" * 70)
print("              REPORTE INICIAL DE CUENTAS (__str__)")
print("=" * 70)
for c in banco:
    print(c)


print("\n" + "=" * 70)
print("             EJECUTANDO CIERRE MENSUAL POLIMÓRFICO")
print("=" * 70)
for c in banco:
    c.cierre_mensual()

print("\n" + "=" * 70)
print("              REPORTE FINAL DE CUENTAS (__str__)")
print("=" * 70)
for c in banco:
    print(c)