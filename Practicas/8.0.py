
def registrar_usuario(nombre, edad, pin):
    if len(nombre.strip()) < 3:
        raise ValueError("El nombre debe tener al menos 3 letras.")
    if edad < 18 or edad > 100:
        raise ValueError("Edad fuera de rango: solo se admiten usuarios entre 18 y 100 años.")
    if len(str(pin)) != 4:
        raise ValueError("El PIN de seguridad debe contener exactamente 4 dígitos.")
    return f"Usuario '{nombre}' registrado exitosamente con PIN configurado."

while True:
    try:
        nombre=(input("Ingrese su nombre: "))
        edad=int(input("Ingrese su edad: "))
        pin=(input("Ingrese su pin: "))
        print(registrar_usuario(nombre, edad, pin))
        break
    except ValueError as e:
        print(f"Error de registro: {e}") 








