#Sistema bancario modular en POO

class CuentaBancaria():

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
            if monto <=0:
                raise ValueError("Error: El monto a depositar debe ser mayor a cero.")
            self.saldo += monto
            print(f"Depósito de ${monto:,.2f} aplicado. Saldo actual: ${self.saldo:,.2f}")
            return self.saldo
            



   def retirar(self, monto):
    if not self.activa:
      raise ValueError("Error: La cuenta no está activa.")
    if monto <= 0:
      raise ValueError("Error: El monto a retirar debe ser positivo y mayor a cero.")
    if monto > self.saldo:
      raise ValueError(f"Error: Saldo insuficiente. Saldo disponible: ${self.saldo:,.2f}")
    self.saldo -= monto
    print(f"Se ha retirado ${monto:,.2f} de la cuenta. Saldo actual: ${self.saldo:,.2f}")
    return self.saldo




   def cierre_mensual(self):
    
            comision = 5.0
            if self.saldo >= comision:
                self.saldo -= comision
                print(f"[{self.numero_cuenta}] Mantenimiento mensual descontado: -${comision:,.2f}")
            else:
                print(f"[{self.numero_cuenta}] Saldo insuficiente para deducir comisión de mantenimiento.")

class CuentaAhorro(CuentaBancaria):
    def __init__(self, numero_cuenta, titular, saldo_inicial=0.0, tasa_interes=0.04):
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
            raise ValueError("Error: El monto a retirar debe ser positivo y mayor a cero.")

        disponible = self.saldo + self.sobregiro
        if monto > disponible:
            raise ValueError(
                f"Error: Saldo insuficiente. Máximo disponible: ${disponible:,.2f}"
            )
        
        self.saldo -= monto
        print(f"[{self.numero_cuenta}] Retiro de ${monto:,.2f} aplicado. Saldo actual: ${self.saldo:,.2f}")
        return self.saldo




    def cierre_mensual(self):
        
        if self.saldo <0:
            recargo= abs(self.saldo)*0.10
            self.saldo -= recargo
            print(f"[{self.numero_cuenta}] Recargo de ${recargo:,.2f} aplicado. Saldo actual: ${self.saldo:,.2f}")
        else:
            super().cierre_mensual()



class Banco:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cuentas = { 
            "CTA-100": CuentaBancaria("CTA-100", "Elena Vega", 500.0),
            "CA-200": CuentaAhorro("CA-200", "Lucía Peña", 1000.0, tasa_interes=0.04),
            "CC-300": CuentaCorriente("CC-300", "Javier Rivas", 200.0, sobregiro=500.0)
        }




    def registar_cuenta(self, cuenta):
        if cuenta.numero_cuenta in self.cuentas:
            raise ValueError(f"Error: Ya existe una cuenta con el número {cuenta.numero_cuenta}")
        self.cuentas[cuenta.numero_cuenta] = cuenta
        print(f"Se ha registrado la cuenta {cuenta.numero_cuenta}")
        



    

    

    def obtener_cuenta(self, numero_cuenta):
        if numero_cuenta not in self.cuentas:
            raise ValueError(f"Error: No existe una cuenta con el número {numero_cuenta}")
        return self.cuentas[numero_cuenta]
        
            
        

    def transferir(self, origen_num, destino_num, monto):

        if origen.numero_cuenta == destino.numero_cuenta:
            raise ValueError("Error: No se puede transferir a la misma cuenta")
        origen = self.obtener_cuenta(origen_num)
        destino = self.obtener_cuenta(destino_num)
        origen.retirar(monto)
        destino.depositar(monto)
        print(f"Transferencia de ${monto:,.2f} completada exitosamente.")
        


        
    def ejecutar_cierre_global(self):
        print("\n" + "=" * 70)
        print("CIERRE GLOBAL.")
        print("=" * 70)
        for cuenta in self.cuentas.values():
            cuenta.cierre_mensual()


    def listar_cuentas(self):
        print("\n" + "=" * 70)
        print("LISTA DE CUENTAS.")
        print("=" * 70)
        print(f"{self.nombre}")
        print("=" * 70)
        print("\n".join([str(c) for c in self.cuentas.values()]))


mi_banco = Banco("Mi Banco")

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
                    print("Error: Tipo de cuenta no reconocido.")
                    continue
            mi_banco.registar_cuenta(nueva_cuenta)


        

        elif opcion == 2:
            mi_banco.listar_cuentas()
        elif opcion == 3:
            num = input("Ingrese el número de la cuenta: ")
            monto = float(input("Ingrese el monto a depositar: "))
            cuenta = mi_banco.obtener_cuenta(num)
            cuenta.depositar(monto)
        elif opcion == 4:
            num = input("Ingrese el número de la cuenta: ")
            monto = float(input("Ingrese el monto a retirar: "))
            cuenta = mi_banco.obtener_cuenta(num)
            cuenta.retirar(monto)
        elif opcion == 5:
            origen_num = input("Ingrese el número de la cuenta de origen: ")
            destino_num = input("Ingrese el número de la cuenta de destino: ")
            monto = float(input("Ingrese el monto a transferir: "))
            mi_banco.transferir(origen_num, destino_num, monto)
        elif opcion == 6:
            mi_banco.ejecutar_cierre_global()
        elif opcion == 7:
            break
    except ValueError as e:
        print(e)