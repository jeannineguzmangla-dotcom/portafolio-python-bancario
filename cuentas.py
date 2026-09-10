class CuentaBancaria:
    def __init__(self, numero_cuenta, titular, saldo_inicial=0.0):
        self.numero_cuenta = numero_cuenta
        self.titular = titular
        self.saldo = 0.0 if saldo_inicial < 0 else saldo_inicial
        self.activa = True

    def __str__(self):
        return f"[{self.numero_cuenta}] Titular: {self.titular:<15} | Saldo: ${self.saldo:>10,.2f}"

    def depositar(self, monto):
        if not self.activa:
            raise ValueError("Error: La cuenta no está activa.")
        if monto <= 0:
            raise ValueError("Error: El monto a depositar debe ser mayor a cero.")
        self.saldo += monto
        print(f"Depósito de ${monto:,.2f} aplicado. Saldo actual: ${self.saldo:,.2f}")
        return self.saldo

    def retirar(self, monto):
        if not self.activa:
            raise ValueError("Error: La cuenta no está activa.")
        if monto <= 0:
            raise ValueError("Error: El monto a retirar debe ser mayor a cero.")
        if monto > self.saldo:
            raise ValueError(f"Error: Saldo insuficiente. Saldo disponible: ${self.saldo:,.2f}")
        self.saldo -= monto
        print(f"Retiro de ${monto:,.2f} aplicado. Saldo actual: ${self.saldo:,.2f}")
        return self.saldo

    def cierre_mensual(self):
        comision = 5.0
        if self.saldo >= comision:
            self.saldo -= comision
            print(f"[{self.numero_cuenta}] Mantenimiento mensual descontado: -${comision:,.2f}")
        else:
            print(f"[{self.numero_cuenta}] Saldo insuficiente para deducir comisión.")


class CuentaAhorro(CuentaBancaria):
    def __init__(self, numero_cuenta, titular, saldo_inicial=0.0, tasa_interes=0.04):
        super().__init__(numero_cuenta, titular, saldo_inicial)
        self.tasa_interes = tasa_interes

    def __str__(self):
        return f"[Ahorro]    [{self.numero_cuenta}] Titular: {self.titular:<15} | Saldo: ${self.saldo:>10,.2f} | Tasa: {self.tasa_interes * 100:.1f}%"

    def aplicar_interes(self):
        intereses = self.saldo * self.tasa_interes
        self.saldo += intereses
        print(f"[{self.numero_cuenta}] Interés abonado (+{self.tasa_interes * 100:.1f}%): +${intereses:,.2f}")

    def cierre_mensual(self):
        self.aplicar_interes()


class CuentaCorriente(CuentaBancaria):
    def __init__(self, numero_cuenta, titular, saldo_inicial=0.0, sobregiro=500.0):
        super().__init__(numero_cuenta, titular, saldo_inicial)
        self.sobregiro = sobregiro

    def __str__(self):
        return f"[Corriente] [{self.numero_cuenta}] Titular: {self.titular:<15} | Saldo: ${self.saldo:>10,.2f} | Sobregiro: ${self.sobregiro:,.2f}"

    def retirar(self, monto):
        if not self.activa:
            raise ValueError("Error: La cuenta no está activa.")
        if monto <= 0:
            raise ValueError("Error: El monto a retirar debe ser mayor a cero.")

        disponible = self.saldo + self.sobregiro
        if monto > disponible:
            raise ValueError(f"Error: Monto excede el límite disponible (${disponible:,.2f}).")

        self.saldo -= monto
        print(f"[{self.numero_cuenta}] Retiro de ${monto:,.2f} aplicado. Saldo actual: ${self.saldo:,.2f}")
        return self.saldo

    def cierre_mensual(self):
        if self.saldo < 0:
            recargo = abs(self.saldo) * 0.10
            self.saldo -= recargo
            print(f"[{self.numero_cuenta}] Recargo por descubierto (10%): -${recargo:,.2f}")
        else:
            super().cierre_mensual()