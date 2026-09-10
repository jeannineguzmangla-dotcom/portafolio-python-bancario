import sqlite3

conexion = sqlite3.connect("banco.db")
cursor = conexion.cursor()

def mostrar_tabla():
    print("-" * 60)
    cursor.execute("SELECT numero_cuenta, titular, saldo FROM cuentas")
    for cuenta, titular, saldo in cursor.fetchall():
        print(f"[{cuenta}] {titular:<15} | Saldo: ${saldo:>10,.2f}")
    print("-" * 60)

print("=== SALDOS ANTES DE LA TRANSFERENCIA ===")
mostrar_tabla()

cuenta_origen = "CTA-100"
cuenta_destino = "CC-300"
monto = 900.0

try:
    cursor.execute("SELECT saldo FROM cuentas WHERE numero_cuenta = ?", (cuenta_origen,))
    resultado = cursor.fetchone()

    if not resultado:
        raise ValueError("La cuenta de origen no existe.")

    saldo_origen = resultado[0]
    if saldo_origen < monto:
        raise ValueError(f"Saldo insuficiente (${saldo_origen:,.2f}) para transferir ${monto:,.2f}.")

    cursor.execute("""
        UPDATE cuentas 
        SET saldo = saldo - ? 
        WHERE numero_cuenta = ?
    """, (monto, cuenta_origen))

    cursor.execute("""
        UPDATE cuentas 
        SET saldo = saldo + ? 
        WHERE numero_cuenta = ?
    """, (monto, cuenta_destino))

    conexion.commit()
    print(f"\nÉxito: Se transfirieron ${monto:,.2f} de {cuenta_origen} a {cuenta_destino}.")

except Exception as error:
    conexion.rollback()
    print(f"\nTransacción abortada (Rollback ejecutado): {error}")

finally:
    print("\n=== SALDOS DESPUÉS DE LA OPERACIÓN ===")
    mostrar_tabla()
    conexion.close()