from sqlalchemy import create_engine, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class CuentaORM(Base):
    __tablename__ = "cuentas_orm"

    numero_cuenta: Mapped[str] = mapped_column(String(20), primary_key=True)
    titular: Mapped[str] = mapped_column(String(100), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    saldo: Mapped[float] = mapped_column(Float, default=0.0)

    def __repr__(self) -> str:
        return f"<Cuenta(numero='{self.numero_cuenta}', titular='{self.titular}', saldo={self.saldo})>"

engine = create_engine("sqlite:///banco_orm.db", echo=False)
Base.metadata.create_all(engine)

with Session(engine) as sesion:
    cuenta_1 = CuentaORM(numero_cuenta="ORM-100", titular="Elena Vega", tipo="Estándar", saldo=500.0)
    cuenta_2 = CuentaORM(numero_cuenta="ORM-200", titular="Lucía Peña", tipo="Ahorro", saldo=1000.0)

    sesion.add_all([cuenta_1, cuenta_2])
    sesion.commit()
    print("Registros creados exitosamente mediante el ORM.")

    print("\n" + "=" * 60)
    print("        CONSULTA ORM (SIN ESCRIBIR SQL PURO)")
    print("=" * 60)

    cuentas = sesion.query(CuentaORM).all()
    for c in cuentas:
        print(f"[{c.numero_cuenta}] Titular: {c.titular:<15} | Saldo: ${c.saldo:>10,.2f}")

    cuenta_a_modificar = sesion.query(CuentaORM).filter_by(numero_cuenta="ORM-100").first()
    if cuenta_a_modificar:
        cuenta_a_modificar.saldo += 150.0
        sesion.commit()
        print(f"\nSaldo actualizado para {cuenta_a_modificar.titular}: ${cuenta_a_modificar.saldo:,.2f}")
        