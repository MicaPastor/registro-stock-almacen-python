import questionary
from datetime import datetime, timedelta
from funciones.menu import seleccionar_categoria
from funciones.archivos import guardar_json, registrar_en_log
from funciones.helpers import seleccionar_producto_por_nombre, formatear_fecha


def ver_stock_completo(stock):
    """
    Muestra todos los productos actualmente en stock, con su información completa y formateada.

    Args:
        stock (dict): Diccionario que contiene los productos del inventario.

    Returns:
        None

    Excepciones:
        No lanza excepciones explícitas.
    """
    #Si el inventario está vacío, se informa y sale
    if not stock:
        print("\n📦 El inventario está vacío.")
        return
    #Título
    print("\n📋 LISTADO COMPLETO DE PRODUCTOS EN STOCK:\n")
    
    #Se recorre cada producto y muestra su información
    for i, (clave, prod) in enumerate(stock.items(), 1):
        print(f"{i}. {clave}")
        print(f"   Categoría: {prod.get('categoria', 'No especificada')}")
        print(f"   Ingreso: {prod.get('fecha_ingreso', 'N/D')} | Vencimiento: {prod.get('vencimiento', 'N/D')}")
        print(f"   Stock: {prod.get('cantidad', '?')} unidades (mínimo: {prod.get('stock_minimo', '?')})")
        print(f"   Precio: ${prod.get('precio', '?')}\n")

def ver_stock_por_categoria(stock):
    """
    Filtra y muestra los productos en stock según la categoría seleccionada por el usuario.

    Utiliza un menú interactivo (`questionary`) para elegir la categoría.

    Args:
        stock (dict): Diccionario con los productos del inventario.

    Returns:
        None

    Excepciones:
        No lanza excepciones explícitas.
    """
    #Si no hay productos en stock, avisa y sale
    if not stock:
        print("\n📦 El inventario está vacío.")
        return
    #Se pide al usuario seleccionar una categoría
    categoria = seleccionar_categoria()  
    #Filtra los productos que coinciden con la categoría seleccionada
    filtrados = {
        clave: datos for clave, datos in stock.items()
        if datos.get("categoria", "").lower() == categoria.lower()
    }
    #Si no hay productos en esa categoría avisa.
    if not filtrados:
        print(f"\n📦 No hay productos en la categoría '{categoria}'.")
        return
    #Muestra productos filtrados
    print(f"\n📋 PRODUCTOS EN CATEGORÍA: {categoria.upper()}\n")

    for i, (clave, datos) in enumerate(filtrados.items(), 1):
        print(f"{i}. {clave}")
        print(f"   Ingreso: {datos['fecha_ingreso']} | Vencimiento: {datos['vencimiento']}")
        print(f"   Stock: {datos['cantidad']} unidades (mínimo: {datos['stock_minimo']})")
        print(f"   Precio: ${datos['precio']}\n")
        
def buscar_producto(stock):
    """
    Permite buscar un producto por nombre (coincidencia parcial) y ver su información completa.

    Utiliza un selector interactivo para que el usuario elija entre los productos encontrados,
    en caso de haber más de una coincidencia.

    Args:
        stock (dict): Diccionario que contiene los productos actuales del inventario.

    Returns:
        None

    Excepciones:
        No lanza excepciones explícitas.
    """
    #Se verifica si hay productos cargados, sino avisa
    if not stock:
        print("\n📦 El inventario está vacío.")
        return
    #Buscamos un producto por nombre y obtenemos su clave
    clave = seleccionar_producto_por_nombre(stock, "ver")
    if not clave:
        print("🔙 Búsqueda cancelada.")
        return
    #Muestra los dato completos del producto seleccionado
    producto = stock[clave]

    print(f"\n🔍 Resultado para '{clave}':")
    print(f"   Nombre: {producto['nombre']}")
    print(f"   Marca: {producto['marca']}")
    print(f"   Presentación: {producto['presentacion']}")
    print(f"   Categoría: {producto.get('categoria', 'No especificada')}")
    print(f"   Fecha de ingreso: {producto['fecha_ingreso']}")
    print(f"   Vencimiento: {producto['vencimiento']}")
    print(f"   Cantidad: {producto['cantidad']} unidades")
    print(f"   Stock mínimo: {producto['stock_minimo']}")
    print(f"   Precio: ${producto['precio']}")
    
def editar_o_eliminar_producto(stock):
    """
    Permite al usuario elegir si desea eliminar o editar un producto del inventario.

    Muestra un menú interactivo con `questionary` para seleccionar la acción deseada.
    En base a la elección, llama a la función correspondiente y devuelve el stock modificado.

    Args:
        stock (dict): Diccionario con los productos actuales del inventario.

    Returns:
        dict: El stock actualizado después de la edición o eliminación. Si el usuario cancela, se devuelve sin cambios.

    Excepciones:
        No lanza excepciones explícitas.
    """
    #Menú para elegir entre editar, eliminar o cancelar
    accion = questionary.select(
        "¿Qué querés hacer?",
        choices=[
            "Eliminar un producto",
            "Editar un producto",
            "Cancelar"
        ]
    ).ask()
    #Se ejecuta la acción correspondiente
    if accion == "Eliminar un producto":
        stock = eliminar_producto(stock)
    elif accion == "Editar un producto":
        stock = editar_producto(stock)
    else:
        print("🔙 Operación cancelada.")
    #Devuelve el stock
    return stock
                     
def eliminar_producto(stock):
    """
    Permite buscar un producto por nombre y eliminarlo del inventario, con confirmación previa.

    Utiliza menús interactivos (`questionary`) para seleccionar el producto y confirmar la eliminación.
    Si se confirma, actualiza el archivo JSON y registra el cambio en el log.

    Args:
        stock (dict): Diccionario con el inventario actual.

    Returns:
        dict: Inventario actualizado sin el producto eliminado. Si el usuario cancela, se devuelve sin cambios.

    Excepciones:
        No lanza excepciones explícitas.
    """
    #Verifica que haya productos, si no avisa.
    if not stock:
        print("\n📦 El inventario está vacío.")
        return stock
    #Selecciona el producto a eliminar
    clave = seleccionar_producto_por_nombre(stock, "eliminar")
    if not clave:
        print("🔙 Operación cancelada.")
        return stock
    #Confirma si desea eliminarlo
    confirmar = questionary.confirm(
    f"¿Estás segura de que querés eliminar '{clave}'?").ask()


    if not confirmar:
        print("❎ Eliminación cancelada.")
        return stock
    #Producto eliminado
    eliminado = stock.pop(clave)
    #Guarda el stock actualizado
    guardar_json(stock)
    #Refistra accion en log
    registrar_en_log(f"🗑 Producto eliminado: '{clave}' ({eliminado['marca']})")
    #Informa al usuario
    print(f"✅ Producto eliminado: {clave}")
    return stock
    
def editar_producto(stock):
    """
    Permite al usuario editar uno de los campos de un producto existente en el inventario.

    Se selecciona el producto por nombre usando coincidencia parcial, y luego se elige 
    qué campo editar. Si el valor ingresado es inválido, se solicita nuevamente. 
    Se aplican validaciones específicas para cada tipo de dato (números y fechas).
    
    Al finalizar, se guardan los cambios en el archivo JSON y se registra la modificación en el log.

    Args:
        stock (dict): Diccionario con el inventario actual.

    Returns:
        dict: El inventario actualizado con los cambios aplicados.

    Excepciones:
        No lanza excepciones explícitas. Maneja los errores de entrada de forma interactiva.
    """
    #Chequeea el stock, si no hay avisa
    if not stock:
        print("\n📦 El inventario está vacío.")
        return stock
    #Selección del producto por nombre
    clave = seleccionar_producto_por_nombre(stock, "editar")
    if not clave:
        print("🔙 Edición cancelada.")
        return stock

    producto = stock[clave]
    
    #Menú de campos disponibles para editar
    campo = questionary.select(
        "¿Qué querés editar?",
        choices=[
            "Marca", "Presentación", "Cantidad", "Precio",
            "Stock mínimo", "Fecha de ingreso", "Fecha de vencimiento", 
            "Categoría", "Cancelar"
        ]
    ).ask()

    if campo == "Cancelar":
        print("🔙 Edición cancelada.")
        return stock
    
    #Por cada campo posible, se pide nuevo valor y valida
    if campo == "Marca":
        producto["marca"] = questionary.text("Nueva marca:").ask()

    elif campo == "Presentación":
        producto["presentacion"] = questionary.text("Nueva presentación:").ask()

    elif campo == "Cantidad":
        while True:
            try:
                producto["cantidad"] = float(questionary.text("Nueva cantidad:").ask())
                break
            except ValueError:
                print("❌ Cantidad inválida. Ingresá un número.")

    elif campo == "Precio":
        while True:
            try:
                producto["precio"] = float(questionary.text("Nuevo precio:").ask())
                break
            except ValueError:
                print("❌ Precio inválido. Ingresá un número con punto.")

    elif campo == "Stock mínimo":
        while True:
            try:
                nuevo_minimo = int(questionary.text("Nuevo stock mínimo:").ask())
                if nuevo_minimo > producto["cantidad"]:
                    print(f"❌ El stock mínimo no puede ser mayor que la cantidad actual ({producto['cantidad']} unidades).")
                else:
                    producto["stock_minimo"] = nuevo_minimo
                    break
            except ValueError:
                print("❌ Valor inválido. Ingresá un número entero.")
 
    elif campo == "Fecha de ingreso":
        while True:
            nueva_fecha = formatear_fecha(questionary.text("Fecha de ingreso (DDMMAAAA):").ask())
            try:
                f = datetime.strptime(nueva_fecha, "%d/%m/%Y")
                if f > datetime.today():
                    print("❌ No puede ser futura.")
                else:
                    producto["fecha_ingreso"] = nueva_fecha
                    break
            except:
                print("❌ Fecha inválida.")

    elif campo == "Fecha de vencimiento":
        while True:
            nueva_fecha = formatear_fecha(questionary.text("Fecha de vencimiento (DDMMAAAA):").ask())
            try:
                f_venc = datetime.strptime(nueva_fecha, "%d/%m/%Y")
                f_ing = datetime.strptime(producto["fecha_ingreso"], "%d/%m/%Y")
                if f_venc < f_ing:
                    print("❌ No puede vencer antes del ingreso.")
                else:
                    producto["vencimiento"] = nueva_fecha
                    break
            except:
                print("❌ Fecha inválida.")

    elif campo == "Categoría":
        producto["categoria"] = seleccionar_categoria()

    #Guarda el stock actualizado y registra en el log
    guardar_json(stock)
    registrar_en_log(f"✏️ Producto editado: '{clave}' (campo: {campo})")
    print("✅ Producto actualizado correctamente.")

    return stock

def agregar_insumos(stock):
    """
    Agrega un nuevo producto al inventario o actualiza uno existente si ya está registrado.

    Los datos del producto se obtienen mediante un formulario interactivo.
    Si el producto ya existe, se suma la cantidad nueva a la existente y se actualiza el precio si es diferente.
    Todos los cambios se registran en el archivo de log y se guardan en el archivo JSON.

    Args:
        stock (dict): Diccionario que representa el inventario actual.

    Returns:
        dict: El inventario actualizado con el nuevo producto o con la modificación aplicada.

    Excepciones:
        No lanza excepciones explícitas. Si se cancela el ingreso, se devuelve el stock sin modificar.
    """
    #Obtiene los datos del nuvp producto
    clave, producto = obtener_datos_producto()

    # Si el ingreso due cancelado o inválidoc, no hace nada.
    if not clave:
        print("❌ No se pudo agregar el producto.")
        return stock
    
    #Si el producto ya existe en el stock
    if clave in stock:
        # Suma cantidad nueva a existente
        stock[clave]["cantidad"] += producto["cantidad"]

        #Si el precio cambió, lo actualiza
        if producto["precio"] != stock[clave]["precio"]:
            stock[clave]["precio"] = producto["precio"]
            registrar_en_log(f"💲 Se actualizó el precio de '{clave}'.")

        registrar_en_log(f"➕ Se agregó cantidad a '{clave}'.")
        print(f"✅ Producto existente actualizado: {clave}")
    # Si el producto no estaba en el stock, lo agrega como nuevo    
    else:
        stock[clave] = producto
        registrar_en_log(f"🆕 Se agregó un nuevo producto: '{clave}'.")
        print(f"✅ Producto nuevo agregado: {clave}")

    guardar_json(stock)
    return stock

def obtener_datos_producto():
    """
    Solicita al usuario los datos para registrar un nuevo producto.

    Cada campo es validado de forma interactiva:
    - La cantidad y el stock mínimo deben ser enteros válidos.
    - El precio debe ser un número decimal.
    - Las fechas deben estar en formato DDMMAAAA y tener lógica (el vencimiento posterior al ingreso).
    - El stock mínimo no puede ser mayor que la cantidad.

    Returns:
        tuple: Una tupla con dos elementos:
            - clave (str): Identificador único generado con nombre, marca y presentación.
            - producto (dict): Diccionario con todos los datos del producto.
    """
    # Recolección de datos básicos del producto
    nombre = questionary.text("Nombre del producto:").ask()
    marca = questionary.text("Marca del producto:").ask()
    presentacion = questionary.text("Presentación (ej: 500ml, 1L, pack x 6):").ask()

    # Generación clave única 
    clave = f"{nombre}({marca}) - {presentacion}"

    # Cantidad con validación
    while True:
        try:
            cantidad = int(questionary.text("Cantidad:").ask())
            break
        except ValueError:
            print("❌ Cantidad inválida. Ingresá un número entero.")

    # Precio con validación
    while True:
        try:
            precio = float(questionary.text("Precio:").ask())
            break
        except ValueError:
            print("❌ Precio inválido. Ingresá un número con punto. Ej: 38.7.")

    # Stock mínimo con validación y comparación
    while True:
        try:
            stock_minimo = int(questionary.text("Cantidad mínima (stock mínimo):").ask())
            if stock_minimo > cantidad:
                print("❌ El stock mínimo no puede ser mayor que la cantidad ingresada.")
            else:
                break
        except ValueError:
            print("❌ Valor inválido. Ingresá un número entero.")

    # Fecha de ingreso
    while True:
        fecha_ingreso = formatear_fecha(questionary.text("Fecha de ingreso (DDMMAAAA):").ask())
        try:
            fecha_obj = datetime.strptime(fecha_ingreso, "%d/%m/%Y")
            if fecha_obj > datetime.today():
                print("❌ La fecha de ingreso no puede ser futura.")
            else:
                break
        except:
            print("❌ Fecha inválida. Ingresá en formato DDMMAAAA.")

    # Fecha de vencimiento, posterior al ingreso
    while True:
        fecha_vencimiento = formatear_fecha(questionary.text("Fecha de vencimiento (DDMMAAAA):").ask())
        try:
            f_venc = datetime.strptime(fecha_vencimiento, "%d/%m/%Y")
            f_ing = datetime.strptime(fecha_ingreso, "%d/%m/%Y")
            if f_venc < f_ing:
                print("❌ La fecha de vencimiento no puede ser anterior al ingreso.")
            else:
                break
        except:
            print("❌ Fecha inválida. Ingresá en formato DDMMAAAA.")

    # Categoría con menú
    categoria = questionary.select(
        "Seleccioná la categoría del producto:",
        choices=["Alimentos", "Bebidas y Lácteos", "Limpieza", "Otros"]
    ).ask()

    # Crear diccionario del producto
    producto = {
        "nombre": nombre,
        "marca": marca,
        "presentacion": presentacion,
        "cantidad": cantidad,
        "precio": precio,
        "stock_minimo": stock_minimo,
        "vencimiento": fecha_vencimiento,
        "fecha_ingreso": fecha_ingreso,
        "categoria": categoria,
    }

    return clave, producto
    
def actualizar_producto_existente(stock, nuevo_producto):
    """
    Actualiza un producto ya existente en el inventario sumando la cantidad 
    y modificando el precio si es diferente.

    El producto se identifica por su campo 'nombre', que debe estar presente como clave en el stock.

    Args:
        stock (dict): Diccionario con el inventario actual.
        nuevo_producto (dict): Diccionario con los datos nuevos del producto (al menos 'nombre', 'cantidad', 'precio').

    Returns:
        dict: El inventario actualizado con los cambios aplicados al producto existente.

    Excepciones:
        KeyError: Si el nombre del producto no se encuentra en el stock.
    """
    #Obtiene el nombre del producto como clave
    nombre = nuevo_producto["nombre"]
    #Suma la cantidad al stock existente
    stock[nombre]["cantidad"] += nuevo_producto["cantidad"]
    #Si el precio cambió, lo actualiza y registra en log
    if nuevo_producto["precio"] != stock[nombre]["precio"]:
        stock[nombre]["precio"] = nuevo_producto["precio"]
        registrar_en_log(f"Precio del producto {nombre} actualizado.")

    return stock

def agregar_producto_nuevo(stock, producto):
    """
    Agrega un nuevo producto al inventario.

    El producto se inserta utilizando su campo 'nombre' como clave del diccionario.

    Args:
    stock (dict): Diccionario que representa el inventario actual.
    producto (dict): Diccionario con los datos del nuevo producto. 
    Debe incluir al menos 'nombre' como clave primaria.

    Returns:
    dict: El inventario actualizado con el nuevo producto agregado.
    """
    stock[producto["nombre"]] = producto
    return stock

def mostrar_avisos(stock):
    """
    Muestra alertas de productos que están vencidos, por vencer en los próximos 7 días,
    o con una cantidad igual o menor al stock mínimo.

    El análisis se hace por fecha actual y compara con la fecha de vencimiento.
    También revisa si la cantidad disponible es menor o igual al stock mínimo.

    Args:
        stock (dict): Diccionario que representa el inventario actual. Cada producto debe tener los campos:
                      'vencimiento', 'cantidad' y 'stock_minimo'.

    Returns:
        None

    Excepciones:
        No lanza excepciones explícitas. Ignora productos con datos incompletos o inválidos.
    """
    # Si no hay stock cargado, no hay nada para analizar
    if not stock:
        print("\n📦 El inventario está vacío.")
        return
    #Calcula la feha actual y el rango para los próximos 7 días.
    hoy = datetime.today()
    proximos_7_dias = hoy + timedelta(days=7)

    vencidos = []
    por_vencer = []
    bajo_stock = []

    #Recorre cada producto del stock
    for producto in stock.values():
        # Valida que tenga los campos necesarios
        if "vencimiento" not in producto or "stock_minimo" not in producto:
            continue

        #Verifica la fecha de vencimiento
        try:
            fecha_venc = datetime.strptime(producto["vencimiento"], "%d/%m/%Y")
            if fecha_venc < hoy:
                vencidos.append(producto)
            elif hoy <= fecha_venc <= proximos_7_dias:
                por_vencer.append(producto)
        except ValueError:
            continue  # Fecha mal cargada

        #Verifica si el producto tiene bajo stock
        try:
            if producto["cantidad"] <= producto["stock_minimo"]:
                bajo_stock.append(producto)
        except:
            continue

    if vencidos:
        print("\n🔴 PRODUCTOS VENCIDOS:")
        for p in vencidos:
            print(f"- {p['nombre']} ({p['marca']}) venció el {p['vencimiento']}")

    if por_vencer:
        print("\n🟠 PRODUCTOS POR VENCER (próximos 7 días):")
        for p in por_vencer:
            print(f"- {p['nombre']} ({p['marca']}) vence el {p['vencimiento']}")

    if bajo_stock:
        print("\n⚠️ PRODUCTOS CON STOCK BAJO:")
        for p in bajo_stock:
            print(f"- {p['nombre']} ({p['marca']}): {p['cantidad']} unidades (mínimo: {p['stock_minimo']})")

    if not (vencidos or por_vencer or bajo_stock):
        print("\n✅ No hay productos vencidos, por vencer ni con bajo stock.")
        
