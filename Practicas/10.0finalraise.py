class CuentaNoEncontradaError(Exception):
    pass

class SaldoInsuficienteError(Exception):
    pass

cuentas = {
    "CTA-01": {"titular": "Ana Gómez", "saldo": 1200.0},
    "CTA-02": {"titular": "Pedro Soto", "saldo": 450.0}
}

def transferir(origen_id, destino_id, monto):
   
    if origen_id not in cuentas or destino_id not in cuentas:
        cuenta_invalida = origen_id if origen_id not in cuentas else destino_id
        raise CuentaNoEncontradaError(f"La cuenta '{cuenta_invalida}' no existe en el sistema.")
    
   
    if origen_id == destino_id:
        raise ValueError("No se puede transferir a la misma cuenta.")
    
    
    if monto <= 0:
        raise ValueError("El monto a transferir debe ser mayor a cero.")
    
  
    if monto > cuentas[origen_id]["saldo"]:
        raise SaldoInsuficienteError(
            f"Saldo insuficiente. {cuentas[origen_id]['titular']} dispone de ${cuentas[origen_id]['saldo']:,.2f}."
        )
    
   
    cuentas[origen_id]["saldo"] -= monto
    cuentas[destino_id]["saldo"] += monto
    
    return cuentas[origen_id]["saldo"]


while True:
    print("\n" + "=" * 40)
    print("      SISTEMA DE TRANSFERENCIAS         ")
    print("=" * 40)
    print(f"Cuentas disponibles: {list(cuentas.keys())}")
    
    try:
        origen_id = input("Ingrese la cuenta de origen: ").strip().upper()
        destino_id = input("Ingrese la cuenta de destino: ").strip().upper()
        monto = float(input("Ingrese el monto a transferir: "))
        
        saldo_restante = transferir(origen_id, destino_id, monto)

    except ValueError as e:
        print(f"Error de valor: {e}")
    except CuentaNoEncontradaError as e:
        print(f"Error de cuenta: {e}")
    except SaldoInsuficienteError as e:
        print(f"Error de fondos: {e}")
    else:
        print("\n¡Transferencia realizada con éxito!")
        print(f"Nuevo saldo cuenta origen ({origen_id}): ${saldo_restante:,.2f}")
        print(f"Nuevo saldo cuenta destino ({destino_id}): ${cuentas[destino_id]['saldo']:,.2f}")
        break
    finally:
        print("-" * 40)
        print("Registro de auditoría completado.")