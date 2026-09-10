inventario = {
    "manzanas": 50,
    "platanos": 30,
    "naranjas": 25,
    "uvas": 40
}

sum(inventario.values())
inventario.update({"manzanas": 60, "peras": 20}) #update es para agregar o modificar un valor de un diccionario
inventario.pop("platanos") #pop es para eliminar un valor de un diccionario
for i, (clave, valor) in enumerate(inventario.items()):
    print(f"{i}: {clave}: {valor}")
print(f"Total de frutas en inventario: {sum(inventario.values())}")
