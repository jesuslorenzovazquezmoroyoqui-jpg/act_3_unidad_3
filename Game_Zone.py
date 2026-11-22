def mostrar_catalogo(catalogo):
    # Muestra los datos principales de cada juego disponible en la tienda.
    print("\n---- Catálogo de Videojuegos GameZone ----")
    for juego in catalogo:
        print(f"{juego['codigo']} - {juego['nombre']} | ${round(juego['precio'], 2):.2f} | Stock: {juego['existencia']}")

def buscar_producto(catalogo, codigo):
    # Busca el producto por su código; devuelve None si no existe.
    for producto in catalogo:
        if producto["codigo"] == codigo:
            return producto
    return None

# Valida que la cantidad sea mayor a 0 y no supere la existencia disponible.
def hay_existencia(existencia, cantidad):
    if cantidad > 0 and cantidad <= existencia:
        return True
    else:
        return False
    
def calcular_importe(precio, cantidad):
    # Calcula el costo de las unidades solicitadas de un producto.
    return precio * cantidad

def actualizar_existencia(existencia, cantidad):
    # Devuelve el stock que queda después de la compra.
    return existencia - cantidad

def calcular_total(subtotal, descuento=0.0, impuesto=0.16):
    # Aplica primero el descuento y luego el impuesto al subtotal.
    subtotal_con_descuento = subtotal - (subtotal * descuento)
    total = subtotal_con_descuento + (subtotal_con_descuento * impuesto)
    return round(total, 2)

# Controla el flujo principal de ventas, carrito e inventario
def main():
    # Catálogo inicial: cada juego incluye código, nombre, precio y existencias.
    catalogo = [
        {"codigo": "G001", "nombre": "DOOM Eternal", "precio": 699.00, "existencia": 5},
        {"codigo": "G002", "nombre": "Minecraft", "precio": 499.00, "existencia": 8},
        {"codigo": "G003", "nombre": "The Legend of Zelda: Tears of the Kingdom", "precio": 1199.00, "existencia": 3},
        {"codigo": "G004", "nombre": "Super Mario Bros. Wonder", "precio": 999.00, "existencia": 4},
        {"codigo": "G005", "nombre": "Hollow Knight", "precio": 249.00, "existencia": 10}
    ]

    while True:
        # Menú principal: permite comprar, consultar el inventario o salir.
        print("\n=== TIENDA GAMEZONE ===")
        print("1. Realizar una compra")
        print("2. Consultar catálogo e inventario")
        print("3. Salir")
        opcion = input("Seleccione una opción (1-3): ").strip()

        if opcion == "1":
            # Cada compra comienza con un carrito vacío y el catálogo visible.
            carrito = []
            mostrar_catalogo(catalogo)

            while True:
                # Se agregan productos hasta que el usuario escriba SALIR.
                codigo = input("\nEscriba el código del juego (o 'SALIR' para finalizar compra): ").strip().upper()
                if codigo == "SALIR":
                    break

                producto = buscar_producto(catalogo, codigo)
                if producto is None:
                    print("El producto no se encuentra en el catálogo.")
                    continue

                try:
                    cantidad = int(input(f"Ingrese la cantidad de {producto['nombre']} que desea comprar: "))
                except ValueError:
                    print("La cantidad debe ser un número entero.")
                    continue

                # Solo se agrega al carrito y se descuenta del inventario si hay stock suficiente.
                if hay_existencia(producto['existencia'], cantidad):
                    importe = calcular_importe(precio=producto['precio'], cantidad=cantidad)
                    carrito.append({
                        "codigo": producto['codigo'],
                        "nombre": producto['nombre'],
                        "cantidad": cantidad,
                        "importe": importe
                    })
                    producto['existencia'] = actualizar_existencia(producto['existencia'], cantidad)
                    print(f"Agregado: {cantidad} x {producto['nombre']} | Importe: ${round(importe, 2):.2f}")
                else:
                    if cantidad <= 0:
                        print("La cantidad debe ser mayor a cero.")
                    else:
                        print(f"Stock insuficiente de {producto['nombre']}. Disponible: {producto['existencia']}")

            if len(carrito) == 0:
                print("\nNo se agregaron productos al carrito.")
            else:
                # Se calcula e imprime el recibo; las compras de $1000 o más reciben 10% de descuento.
                print("\n========== RECIBO DE COMPRA ==========")
                for item in carrito:
                    print(f"{item['cantidad']} x {item['nombre']} -> ${round(item['importe'], 2):.2f}")
                print("--------------------------------------")

                subtotal = sum(item['importe'] for item in carrito)
                if subtotal >= 1000:
                    porcentaje_desc = 0.10
                    total = calcular_total(subtotal, descuento=0.10)
                else:
                    porcentaje_desc = 0.0
                    total = calcular_total(subtotal)

                monto_descuento = subtotal * porcentaje_desc
                monto_impuesto = (subtotal - monto_descuento) * 0.16

                print(f"Subtotal:              ${round(subtotal, 2):.2f}")
                print(f"Descuento aplicado:   -${round(monto_descuento, 2):.2f}")
                print(f"Impuesto (16%):       +${round(monto_impuesto, 2):.2f}")
                print(f"TOTAL A PAGAR:         ${round(total, 2):.2f}")
                print("======================================")

                # Al terminar, muestra el inventario actualizado tras descontar los artículos vendidos.
                print("\n--- INVENTARIO RESTANTE ---")
                mostrar_catalogo(catalogo)

        elif opcion == "2":
            # Esta consulta solo muestra el catálogo y no modifica las existencias.
            mostrar_catalogo(catalogo)

        elif opcion == "3":
            print("Gracias por visitar GameZone. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Elija 1, 2 o 3.")

main()