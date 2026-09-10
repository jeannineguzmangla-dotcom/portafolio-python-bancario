from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from banco import Banco
from cuentas import CuentaBancaria, CuentaAhorro, CuentaCorriente

# 1. Inicialización de la aplicación FastAPI
app = FastAPI(
    title="API Sistema Bancario",
    description="API REST modular para administración de cuentas y transacciones financieras",
    version="1.0.0"
)

# 2. Instancia global del controlador bancario (con persistencia SQLite)
banco = Banco("Banco Central")


# ==========================================================
# 3. Modelos Pydantic (Validación automática del Body JSON)
# ==========================================================
class CuentaCrearSchema(BaseModel):
    numero_cuenta: str = Field(..., min_length=4, examples=["CTA-500"])
    titular: str = Field(..., min_length=3, examples=["Andrés López"])
    tipo: str = Field(..., examples=["Estándar"])  # Estándar, Ahorro, Corriente
    saldo_inicial: float = Field(default=0.0, ge=0.0, examples=[500.0])


class TransferenciaSchema(BaseModel):
    cuenta_origen: str = Field(..., examples=["CTA-100"])
    cuenta_destino: str = Field(..., examples=["CC-300"])
    monto: float = Field(..., gt=0.0, examples=[50.0])


class MontoOperacionSchema(BaseModel):
    monto: float = Field(..., gt=0.0, examples=[100.0])


# ==========================================================
# 4. Endpoints de la API
# ==========================================================
@app.get("/", tags=["Diagnóstico"])
def estado_servidor():
    """Verifica la conectividad con el servidor backend."""
    return {
        "estado": "activo",
        "banco": banco.nombre,
        "documentacion": "/docs"
    }


@app.get("/cuentas", tags=["Cuentas"])
def listar_todas_las_cuentas():
    """Retorna la lista de todas las cuentas registradas en el sistema."""
    catalogo = []
    for c in banco.cuentas.values():
        catalogo.append({
            "numero_cuenta": c.numero_cuenta,
            "titular": c.titular,
            "saldo": c.saldo,
            "tipo": c.__class__.__name__,
            "activa": c.activa
        })
    return {"total": len(catalogo), "cuentas": catalogo}


@app.get("/cuentas/{numero_cuenta}", tags=["Cuentas"])
def consultar_cuenta(numero_cuenta: str):
    """Consulta el saldo y estado de una cuenta por su identificador único."""
    try:
        cuenta = banco.obtener_cuenta(numero_cuenta)
        return {
            "numero_cuenta": cuenta.numero_cuenta,
            "titular": cuenta.titular,
            "saldo": cuenta.saldo,
            "tipo": cuenta.__class__.__name__,
            "activa": cuenta.activa
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.post("/cuentas", status_code=status.HTTP_201_CREATED, tags=["Cuentas"])
def registrar_nueva_cuenta(datos: CuentaCrearSchema):
    """Crea una nueva cuenta bancaria y la persiste en SQLite."""
    tipo_normalizado = datos.tipo.strip().capitalize()

    if tipo_normalizado == "Ahorro":
        nueva = CuentaAhorro(datos.numero_cuenta, datos.titular, datos.saldo_inicial)
    elif tipo_normalizado == "Corriente":
        nueva = CuentaCorriente(datos.numero_cuenta, datos.titular, datos.saldo_inicial)
    elif tipo_normalizado in ["Estandar", "Estándar"]:
        nueva = CuentaBancaria(datos.numero_cuenta, datos.titular, datos.saldo_inicial)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de cuenta inválido. Opciones: 'Estándar', 'Ahorro', 'Corriente'."
        )

    try:
        banco.registrar_cuenta(nueva)
        return {
            "mensaje": "Cuenta registrada y persistida exitosamente.",
            "cuenta": {
                "numero_cuenta": nueva.numero_cuenta,
                "titular": nueva.titular,
                "saldo": nueva.saldo,
                "tipo": nueva.__class__.__name__
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/transacciones/transferir", tags=["Transacciones"])
def procesar_transferencia(datos: TransferenciaSchema):
    """Ejecuta una transferencia atómica auditada entre dos cuentas."""
    try:
        banco.transferir(datos.cuenta_origen, datos.cuenta_destino, datos.monto)
        return {
            "mensaje": "Transferencia ejecutada y asentada en la base de datos.",
            "origen": datos.cuenta_origen,
            "destino": datos.cuenta_destino,
            "monto": datos.monto
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/operaciones/cierre-global", tags=["Administración"])
def ejecutar_cierre_contable():
    """Aplica intereses y comisiones de mantenimiento mensual a todas las cuentas."""
    try:
        banco.ejecutar_cierre_global()
        return {"mensaje": "Cierre contable global ejecutado correctamente en disco."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/cuentas/{numero_cuenta}/depositar", tags=["Transacciones"])
def depositar_fondos(numero_cuenta: str, datos: MontoOperacionSchema):
    """Abona saldo a una cuenta específica."""
    try:
        cuenta = banco.obtener_cuenta(numero_cuenta)
        nuevo_saldo = cuenta.depositar(datos.monto)
        # Sincronizar en SQLite
        with banco._conectar() as con:
            con.execute(
                "UPDATE cuentas SET saldo = ? WHERE numero_cuenta = ?",
                (nuevo_saldo, numero_cuenta),
            )
            con.execute(
                """
                INSERT INTO movimientos (numero_cuenta, tipo_operacion, monto)
                VALUES (?, 'DEPOSITO', ?)
            """,
                (numero_cuenta, datos.monto),
            )
            con.commit()
        return {
            "mensaje": f"Depósito de ${datos.monto:,.2f} exitoso.",
            "numero_cuenta": numero_cuenta,
            "saldo_actual": nuevo_saldo,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@app.post("/cuentas/{numero_cuenta}/retirar", tags=["Transacciones"])
def retirar_fondos(numero_cuenta: str, datos: MontoOperacionSchema):
    """Retira fondos respetando las reglas de saldo y sobregiro."""
    try:
        cuenta = banco.obtener_cuenta(numero_cuenta)
        nuevo_saldo = cuenta.retirar(datos.monto)
        # Sincronizar en SQLite
        with banco._conectar() as con:
            con.execute(
                "UPDATE cuentas SET saldo = ? WHERE numero_cuenta = ?",
                (nuevo_saldo, numero_cuenta),
            )
            con.execute(
                """
                INSERT INTO movimientos (numero_cuenta, tipo_operacion, monto)
                VALUES (?, 'RETIRO', ?)
            """,
                (numero_cuenta, datos.monto),
            )
            con.commit()
        return {
            "mensaje": f"Retiro de ${datos.monto:,.2f} exitoso.",
            "numero_cuenta": numero_cuenta,
            "saldo_actual": nuevo_saldo,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@app.get("/cuentas/{numero_cuenta}/movimientos", tags=["Auditoría"])
def consultar_movimientos_cuenta(numero_cuenta: str):
    """Obtiene el historial de movimientos auditados de una cuenta bancaria."""
    # Verificar existencia de la cuenta
    banco.obtener_cuenta(numero_cuenta)

    with banco._conectar() as con:
        cursor = con.cursor()
        cursor.execute(
            """
            SELECT id, tipo_operacion, monto, fecha 
            FROM movimientos 
            WHERE numero_cuenta = ? 
            ORDER BY id DESC
        """,
            (numero_cuenta,),
        )
        registros = cursor.fetchall()

    historial = [
        {"id": f[0], "tipo": f[1], "monto": f[2], "fecha": f[3]}
        for f in registros
    ]

    return {
        "numero_cuenta": numero_cuenta,
        "total_movimientos": len(historial),
        "movimientos": historial,
    }