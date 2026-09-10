while True:
    try:
        distancia_kilometros = float(input("Ingrese la distancia en kilómetros: "))
        tiempo_horas = float(input("Ingrese el tiempo transcurrido en horas: "))
        if tiempo_horas <= 0:
            print("El tiempo debe ser mayor que cero. Por favor, ingrese un valor válido.")
            continue
        velocidad=distancia_kilometros / tiempo_horas
        print(f"La velocidad promedio es: {velocidad:.2f} km/h")
        break
    except ValueError:
        print("Entrada inválida. Por favor, ingrese un número válido.")
    except ZeroDivisionError:
        print("El tiempo no puede ser cero. Por favor, ingrese un valor válido.")