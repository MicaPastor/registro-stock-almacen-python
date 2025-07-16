from funciones.menu import mostrar_menu
from funciones.stock import agregar_insumos, ver_stock_completo, ver_stock_por_categoria, buscar_producto, mostrar_avisos, editar_o_eliminar_producto
from funciones.archivos import leer_json


def ejecutar_menu():
    """
    Ejecuta el menú principal del sistema de control de stock.
    Al iniciar, muestra los avisos de productos vencidos, por vencer o con bajo stock.
    Luego, entra en un bucle que permite al usuario navegar por las distintas funciones
    del sistema: agregar productos, ver el inventario, buscar, editar, eliminar o
    volver a consultar los avisos. Finaliza cuando se elige la opción "Salir".

    """
    stock = leer_json()
    
    mostrar_avisos(stock) #muestra avisos al inicio del programa
    
    while True:
        opcion = mostrar_menu()

        if opcion == "Agregar producto":
            stock = agregar_insumos(stock)
        elif opcion == "Ver stock completo":
            ver_stock_completo(stock)
        elif opcion == "Ver por categoría":
            ver_stock_por_categoria(stock)
        elif opcion == "Buscar producto":
            buscar_producto(stock)
        elif opcion == "Eliminar o editar producto":
            stock = editar_o_eliminar_producto(stock)
        elif opcion == "Avisos (vencimiento / bajo stock)":
            mostrar_avisos(stock)
        elif opcion == "Salir":
            print("👋 Hasta luego")
            break
        else:
            print("❌ Opción inválida")
            
ejecutar_menu()
