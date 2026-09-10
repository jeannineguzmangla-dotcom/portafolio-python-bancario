empleados = {
    "EMP01": {"nombre": "Andrea", "departamento": "Ventas", "salario": 1200.0},
    "EMP02": {"nombre": "Carlos", "departamento": "TI", "salario": 1800.0},
    "EMP03": {"nombre": "Sofía", "departamento": "TI", "salario": 2100.0},
    "EMP04": {"nombre": "David", "departamento": "Finanzas", "salario": 1500.0}
}

empleados["EMP01"]["salario"] *= 1.10  # Aumentar el salario de Andrea en un 10%
total_salarios = sum(info["salario"] for info in empleados.values())
for emp_id, info in empleados.items():
    print(f"ID: {emp_id} | Nombre: {info['nombre']} | Departamento: {info['departamento']} | Salario: {info['salario']}")
print(f"Total de salarios: {total_salarios}")