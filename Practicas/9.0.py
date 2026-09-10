class FondosInsuficientesError(Exception):
    pass


class LimiteExcedidoError(Exception):
    pass


def procesar_retiro(saldo_disponible, monto_retiro, limite_diario=1000.0):
    if monto_retiro <= 0:
        raise ValueError("El monto a retirar debe ser mayor a cero.")
    elif monto_retiro > limite_diario:
        raise LimiteExcedidoError(
            f"El monto de ${monto_retiro:,.2f} supera el límite diario de retiro (${limite_diario:,.2f})."
        )
    elif monto_retiro > saldo_disponible:
        raise FondosInsuficientesError(
            f"Fondos insuficientes. Saldo actual: ${saldo_disponible:,.2f}."
        )
    else:
       return saldo_disponible - monto_retiro
        


saldo_disponible = 1500.0
while True:
    monto_retiro = float(input("Ingrese el monto a retirar: "))
    try:
        saldo_disponible = procesar_retiro(saldo_disponible, monto_retiro)
    except ValueError as e:
        print(f"Error, Ingrese un monto valido, no letras: {e}")
    except LimiteExcedidoError as e:
        print(f"Error, El monto excede el limite diario: {e}")
    except FondosInsuficientesError as e:
        print(f"Error, No hay fondos suficientes: {e}")
    else:
        print(f"Retiro realizado con éxito. Saldo actual: ${saldo_disponible:,.2f}.")
        break



        