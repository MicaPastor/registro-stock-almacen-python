import questionary


def seleccionar_producto_por_nombre(stock, accion="ver"):
    """
    Permite al usuario seleccionar un producto del stock mediante búsqueda por nombre (coincidencia parcial).

    Si se encuentran múltiples coincidencias, se muestra un menú interactivo para elegir. Si solo hay una coincidencia, se selecciona automáticamente.

    Args:
        stock (dict): Diccionario que contiene los productos actuales.
        accion (str): Texto para personalizar el mensaje al usuario (por defecto: "ver").

    Retorna:
        str or None: Clave del producto seleccionado, o None si no se encuentra, se cancela o el inventario está vacío.

    Excepciones:
        No lanza excepciones explícitas.
    """
    #Si no hay productos, se informa y sale
    if not stock:
        print("\n📦 El inventario está vacío.")
        return None
    #Se pide al usuario que ingrese el nombre del producto
    termino = questionary.text(f"🔍 ¿Qué producto querés {accion}? (nombre)").ask()
    termino = termino.lower()
    #Se filtran los productos que contienen el término buscado
    coincidencias = {
        clave: datos for clave, datos in stock.items()
        if termino in datos["nombre"].lower()
    }
    #Si no hay coincidencias, se informa y sale
    if not coincidencias:
        print("❌ No se encontraron productos.")
        return None
    #Si hay solo una coincidencia, la devuelve automáticamente
    if len(coincidencias) == 1:
        return next(iter(coincidencias))
    #Si hay varias, se muestra una lista para que el usuario elija
    seleccion = questionary.select(
        f"Varios productos coinciden. Elegí uno para {accion}:",
        choices=list(coincidencias.keys()) + ["Cancelar"]
    ).ask()

    return None if seleccion == "Cancelar" else seleccion


def formatear_fecha(fecha_str):
    """
    Da formato legible a una fecha ingresada como cadena de 8 dígitos.
    Si la fecha está en formato 'DDMMAAAA' (por ejemplo, '14072025'),
    la convierte a formato 'DD/MM/AAAA'. Si no cumple el formato esperado,
    la devuelve tal como fue ingresada.

    Args:
        fecha_str (str): Cadena que representa una fecha, idealmente de 8 dígitos.

    Returns:
        str: Fecha formateada como 'DD/MM/AAAA' o el valor original si no es válida.

    Raises:
        TypeError: Si el argumento no es una cadena.

    """
    #Se verifica que el dato sea texto
    if not isinstance(fecha_str, str):
        raise TypeError("La fecha debe ser una cadena de texto.")
    #Si tiene 8 dígitos numéricos, se formatea como DD/MM/AAAA
    if len(fecha_str) == 8 and fecha_str.isdigit():
        return f"{fecha_str[:2]}/{fecha_str[2:4]}/{fecha_str[4:]}"
    #Si no cumple con el formato esperado, devuelve valor original.
    return fecha_str


