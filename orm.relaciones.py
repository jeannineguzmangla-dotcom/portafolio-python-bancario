from datetime import datetime
from typing import List
from sqlalchemy import DateTime, Float, ForeignKey, String, create_engine, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)


# 1. Base declarativa
class Base(DeclarativeBase):
    pass


# 2. Modelo Padre (Cuenta)
class CuentaORM(Base):
    __tablename__ = "cuentas_bancarias"

    numero_cuenta: Mapped[str] = mapped_column(String(20), primary_key=True)
    titular: Mapped[str] = mapped_column(String(100), nullable=False)
    saldo: Mapped[float] = mapped_column(Float, default=0.0)

    # Relación bidireccional hacia MovimientoORM
    movimientos: Mapped[List["MovimientoORM"]] = relationship(
        back_populates="cuenta", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Cuenta {self.numero_cuenta} | {self.titular} | Saldo: ${self.saldo:,.2f}>"


# 3. Modelo Hijo (Movimiento / Auditoría)
class MovimientoORM(Base):
    __tablename__ = "movimientos_bancarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    numero_cuenta: Mapped[str] = mapped_column(
        ForeignKey("cuentas_bancarias.numero_cuenta"), nullable=False
    )
    tipo_operacion: Mapped[str] = mapped_column(String(30), nullable=False)
    monto: Mapped[float] = mapped_column(Float, nullable=False)
    fecha: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    # Relación inversa hacia la cuenta propietaria
    cuenta: Mapped["CuentaORM"] = relationship(back_populates="movimientos")

    def __repr__(self) -> str:
        return f"<Movimiento #{self.id}: {self.tipo_operacion} de ${self.monto:,.2f}>"


# 4. Configurar motor y tablas
engine = create_engine("sqlite:///banco_relacional.db", echo=False)
Base.metadata.create_all(engine)

# 5. Flujo transaccional con objetos enlazados
with Session(engine) as sesion:
    # A. Crear la cuenta
    cuenta = CuentaORM(
        numero_cuenta="CTA-900", titular="Mariana Salas", saldo=1200.0
    )

    # B. Registrar operaciones adjuntándolas directamente a la colección de la cuenta
    deposito = MovimientoORM(tipo_operacion="DEPOSITO", monto=500.0)
    retiro = MovimientoORM(tipo_operacion="RETIRO_CAJERO", monto=200.0)

    # El ORM asocia automáticamente la foreign key de ambos movimientos a "CTA-900"
    cuenta.movimientos.append(deposito)
    cuenta.movimientos.append(retiro)
    cuenta.saldo += 500.0 - 200.0

    # Persistir todo en una sola transacción atómica
    sesion.add(cuenta)
    sesion.commit()
    print("Cuenta y movimientos asociados persistidos con éxito.")

# 6. Consulta y navegación relacional
with Session(engine) as sesion:
    cuenta_consultada = (
        sesion.query(CuentaORM).filter_by(numero_cuenta="CTA-900").first()
    )

    print("\n" + "=" * 70)
    print(f"DATOS DE LA CUENTA: {cuenta_consultada}")
    print("=" * 70)
    print("HISTORIAL DE MOVIMIENTOS VINCULADOS:")

    # Navegación directa: accedemos a los movimientos como un atributo de lista de Python
    for mov in cuenta_consultada.movimientos:
        print(
            f"  ID #{mov.id:<2} | Fecha: {mov.fecha} | Operación: {mov.tipo_operacion:<15} | Monto: ${mov.monto:>8,.2f}"
        )
    print("=" * 70)