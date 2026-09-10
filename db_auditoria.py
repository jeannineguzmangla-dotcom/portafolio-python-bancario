import sqlite3

conexion = sqlite3.connect("banco.db")
conexion.execute("PRAGMA foreign_keys = ON;")
cursor = conexion.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_cuenta TEXT NOT NULL,
        tipo_operacion TEXT NOT NULL,
        monto REAL NOT NULL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (numero_cuenta) REFERENCES cuentas (numero_cuenta)
    )
""")
conexion.commit()

cuenta_origen = "CTA-100"
cuenta_destino = "CC-300"
monto = 50.0

try:

    cursor.execute(
        "SELECT saldo FROM cuentas WHERE numero_cuenta = ?", (cuenta_origen,)
        )
    resultado = cursor.fetchone()
    if not resultado or resultado[0] < monto:
        raise ValueError("Saldo insuficiente o cuenta inexistente.")

    cursor.execute(
        "UPDATE cuentas SET saldo = saldo - ? WHERE numero_cuenta = ?",
        (monto, cuenta_origen),
    )

    cursor.execute(
        "UPDATE cuentas SET saldo = saldo + ? WHERE numero_cuenta = ?",
        (monto, cuenta_destino),
    )

    cursor.execute(
        """
        INSERT INTO movimientos (numero_cuenta, tipo_operacion, monto)
        VALUES (?, 'TRANSFERENCIA_SALIDA', ?)
    """,
        (cuenta_origen, monto),
    )

    cursor.execute(
        """
        INSERT INTO movimientos (numero_cuenta, tipo_operacion, monto)
        VALUES (?, 'TRANSFERENCIA_ENTRADA', ?)
    """,
        (cuenta_destino, monto),
    )

    conexion.commit()
    print(
        f"Transferencia de ${monto:,.2f} auditada y completada correctamente."
    )

except Exception as error:
    conexion.rollback()
    print(f"Error en la transacción: {error}")

print("\n" + "=" * 75)
print("             REGISTRO HISTÓRICO DE AUDITORÍA (INNER JOIN)")
print("=" * 75)

cursor.execute("""
    SELECT 
        m.id,
        m.fecha,
        c.titular,
        m.numero_cuenta,
        m.tipo_operacion,
        m.monto
    FROM movimientos m
    INNER JOIN cuentas c ON m.numero_cuenta = c.numero_cuenta
    ORDER BY m.id DESC
""")

for fila in cursor.fetchall():
    mov_id, fecha, titular, cuenta, operacion, cant = fila
    print(
        f"#{mov_id:<3} | {fecha} | {cuenta} ({titular:<12}) | {operacion:<22} | ${cant:>8,.2f}"
    )

print("=" * 75)

conexion.close()

