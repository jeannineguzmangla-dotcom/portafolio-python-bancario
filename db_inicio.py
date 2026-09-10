import sqlite3

conexion = sqlite3.connect("banco.db")
cursor = conexion.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS cuentas (
        numero_cuenta TEXT PRIMARY KEY,
        titular TEXT NOT NULL,
        tipo TEXT NOT NULL,
        saldo REAL NOT NULL
    )
""")
conexion.commit()

cuentas_semilla = [
    ("CTA-100", "Elena Vega", "Estándar", 500.0),
    ("CA-200", "Lucía Peña", "Ahorro", 1000.0),
    ("CC-300", "Javier Rivas", "Corriente", 200.0)
]

cursor.executemany("""
    INSERT OR IGNORE INTO cuentas (numero_cuenta, titular, tipo, saldo)
    VALUES (?, ?, ?, ?)
""", cuentas_semilla)
conexion.commit()

print("=" * 65)
print("           REGISTROS EN LA BASE DE DATOS (banco.db)")
print("=" * 65)

cursor.execute("SELECT numero_cuenta, titular, tipo, saldo FROM cuentas")
filas = cursor.fetchall()

for fila in filas:
    num, titular, tipo, saldo = fila
    print(f"[{num}] {titular:<15} | Tipo: {tipo:<9} | Saldo: ${saldo:>10,.2f}")

print("=" * 65)

conexion.close()

