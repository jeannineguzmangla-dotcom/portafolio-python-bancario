import sqlite3
from cuentas import CuentaAhorro, CuentaBancaria, CuentaCorriente


class Banco:

    def __init__(self, nombre, db_path="banco.db"):
        self.nombre = nombre
        self.db_path = db_path
        self.cuentas = {}

        self._inicializar_tablas()
        self._cargar_cuentas_desde_db()

    def _conectar(self):
        """Crea y retorna una conexión con claves foráneas activas."""
        conexion = sqlite3.connect(self.db_path)
        conexion.execute("PRAGMA foreign_keys = ON;")
        return conexion

    def _inicializar_tablas(self):
        """Garantiza la existencia del esquema de datos."""
        with self._conectar() as con:
            cursor = con.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cuentas (
                    numero_cuenta TEXT PRIMARY KEY,
                    titular TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    saldo REAL NOT NULL
                )
            """)
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
            con.commit()

    def _cargar_cuentas_desde_db(self):
        """Rehidrata los objetos desde la base de datos hacia la memoria."""
        with self._conectar() as con:
            cursor = con.cursor()
            cursor.execute(
                "SELECT numero_cuenta, titular, tipo, saldo FROM cuentas"
            )
            filas = cursor.fetchall()

            for num, titular, tipo, saldo in filas:
                if tipo == "Ahorro":
                    objeto_cuenta = CuentaAhorro(num, titular, saldo)
                elif tipo == "Corriente":
                    objeto_cuenta = CuentaCorriente(num, titular, saldo)
                else:
                    objeto_cuenta = CuentaBancaria(num, titular, saldo)

                self.cuentas[num] = objeto_cuenta

    def registrar_cuenta(self, cuenta):
        """Guarda la cuenta tanto en memoria como en banco.db."""
        if cuenta.numero_cuenta in self.cuentas:
            raise ValueError(
                f"Error: Ya existe una cuenta con el número '{cuenta.numero_cuenta}'."
            )

        # Detectar el tipo de cuenta para la columna relacional
        if isinstance(cuenta, CuentaAhorro):
            tipo_txt = "Ahorro"
        elif isinstance(cuenta, CuentaCorriente):
            tipo_txt = "Corriente"
        else:
            tipo_txt = "Estándar"

        with self._conectar() as con:
            cursor = con.cursor()
            cursor.execute(
                """
                INSERT INTO cuentas (numero_cuenta, titular, tipo, saldo)
                VALUES (?, ?, ?, ?)
            """,
                (cuenta.numero_cuenta, cuenta.titular, tipo_txt, cuenta.saldo),
            )
            con.commit()

        self.cuentas[cuenta.numero_cuenta] = cuenta
        print(
            f"Cuenta {cuenta.numero_cuenta} persistida en base de datos exitosamente."
        )

    def obtener_cuenta(self, numero_cuenta):
        if numero_cuenta not in self.cuentas:
            raise ValueError(f"Error: La cuenta '{numero_cuenta}' no existe.")
        return self.cuentas[numero_cuenta]

    def transferir(self, origen_num, destino_num, monto):
        """Transfiere fondos actualizando memoria, tabla cuentas y auditoría de forma atómica."""
        if origen_num == destino_num:
            raise ValueError("Error: No se puede transferir a la misma cuenta.")

        origen = self.obtener_cuenta(origen_num)
        destino = self.obtener_cuenta(destino_num)

        # Intentar el retiro en memoria (valida si hay saldo disponible)
        origen.retirar(monto)
        destino.depositar(monto)

        # Si el retiro en memoria no lanzó excepción, sincronizamos en base de datos
        conexion = self._conectar()
        try:
            cursor = conexion.cursor()

            # 1. Actualizar saldos en memoria y tabla cuentas
            cursor.execute(
                "UPDATE cuentas SET saldo = ? WHERE numero_cuenta = ?",
                (origen.saldo, origen_num),
            )
            cursor.execute(
                "UPDATE cuentas SET saldo = ? WHERE numero_cuenta = ?",
                (destino.saldo, destino_num),
            )

            # 2. Asentar registros de auditoría
            cursor.execute(
                """
                INSERT INTO movimientos (numero_cuenta, tipo_operacion, monto)
                VALUES (?, 'TRANSFERENCIA_SALIDA', ?)
            """,
                (origen_num, monto),
            )
            cursor.execute(
                """
                INSERT INTO movimientos (numero_cuenta, tipo_operacion, monto)
                VALUES (?, 'TRANSFERENCIA_ENTRADA', ?)
            """,
                (destino_num, monto),
            )

            conexion.commit()
            print(
                f"Transferencia de ${monto:,.2f} persistida y auditada en la base de datos."
            )

        except Exception as e:
            conexion.rollback()
            # En caso de falla en BD, revertimos los objetos en memoria
            origen.saldo += monto
            destino.saldo -= monto
            raise ValueError(f"Error al sincronizar con la base de datos: {e}")
        finally:
            conexion.close()

    def ejecutar_cierre_global(self):
        """Aplica el cierre mensual a todos los objetos y actualiza banco.db."""
        print(f"\n--- Ejecutando Cierre Global en {self.nombre} ---")
        with self._conectar() as con:
            cursor = con.cursor()
            for cuenta in self.cuentas.values():
                cuenta.cierre_mensual()
                cursor.execute(
                    "UPDATE cuentas SET saldo = ? WHERE numero_cuenta = ?",
                    (cuenta.saldo, cuenta.numero_cuenta),
                )
            con.commit()
        print("Saldos actualizados en la base de datos tras el cierre mensual.")

    def listar_cuentas(self):
        print("\n" + "=" * 65)
        print(f"              CATÁLOGO DE CUENTAS - {self.nombre.upper()}")
        print("=" * 65)
        for cuenta in self.cuentas.values():
            print(cuenta)
        print("=" * 65)