import questionary

def mostrar_menu():
    """
    Muestra el menú principal de opciones y devuelve la selección del usuario.

    Utiliza la librería `questionary` para presentar un menú interactivo en consola,
    permitiendo elegir una acción sobre el inventario.

    Returns:
        str or None: La opción seleccionada, o None si el usuario cancela.

    Nota:
        Esta función no lanza excepciones explícitas, pero puede devolver None si hay un error de entrada.

    """
    return questionary.select(
        "¿Tarea a realizar?",
        choices=[
            "Agregar producto",
            "Ver stock completo",
            "Ver por categoría",
            "Buscar producto",
            "Eliminar o editar producto",
            "Avisos (vencimiento / bajo stock)",
            "Salir"
        ]
    ).ask()
    

def seleccionar_categoria():
    """
    Muestra un menú interactivo para que el usuario seleccione una categoría de producto.

    Utiliza la librería `questionary` para presentar las opciones disponibles.

    Returns:
        str: La categoría seleccionada por el usuario.

    """
    return questionary.select(
        "Seleccioná la categoría del producto:",
        choices=[
            "Alimentos",
            "Productos de limpieza",
            "Bebidas y lácteos",
            "Otros"
        ]
    ).ask()
    