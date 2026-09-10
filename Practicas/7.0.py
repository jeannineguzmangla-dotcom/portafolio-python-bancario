while True:
    try:
        total_pagar= float(input("Ingrese el total a pagar: "))
        cantidad_comensales= int(input("Ingrese la cantidad de comensales: "))
        pago_individual= total_pagar / cantidad_comensales
        
    except ValueError:
        print("Error: Por favor ingrese un número válido.")
    except ZeroDivisionError:
        print("Error: La cantidad de comensales no puede ser cero. Por favor, ingrese un valor válido.")
    else:
        print(f"El pago individual por comensal es: {pago_individual:.2f}")
        break
    finally:
        print("Verificación de transacción finalizada.")