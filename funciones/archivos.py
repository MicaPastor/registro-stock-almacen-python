import json
from datetime import datetime
import os

RUTA_JSON = "Data/stock.json"
RUTA_LOG = "Data/registro.log"

def leer_json():
    """
    Lee el archivo 'stock.json' y devuelve su contenido como un diccionario.

    Retorna:
        dict: Los datos leídos desde el archivo JSON. Si el archivo no existe 
        o contiene datos inválidos, se retorna un diccionario vacío.

    Excepciones:
        json.JSONDecodeError: Si el contenido del archivo no es JSON válido.
        FileNotFoundError: No se lanza, ya que se maneja devolviendo {}.
    
    Nota:
        No recibe parámetros.
    """
    if not os.path.exists(RUTA_JSON):
        return {}

    with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            return {}

def guardar_json(stock):
    """
    Guarda el inventario completo en el archivo 'stock.json'.

    Args:
        stock (dict): Diccionario que contiene todo el inventario actual.

    Retorna:
        None

    Excepciones:
        Puede lanzar IOError si ocurre un error al escribir el archivo.
    """
    with open(RUTA_JSON, "w", encoding="utf-8") as archivo:
        json.dump(stock, archivo, indent=4, ensure_ascii=False)

def registrar_en_log(mensaje):
    """
    Registra un mensaje en el archivo de log con la fecha y hora actual (dd/mm/aaaa hh:mm:ss).

    Args:
        mensaje (str): Texto que se desea registrar en el archivo de log.

    Retorna:
        None

    Excepciones:
        TypeError: Si el mensaje no es una cadena de texto.
        IOError: Si ocurre un error al intentar escribir en el archivo.
    """
    #se valida que el mensaje sea texto
    if not isinstance(mensaje, str):
        raise TypeError("El mensaje debe ser una cadena de texto.")

    #Se formatea la fecha y arma la línea para guardar.
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linea = f"[{fecha}] {mensaje}\n"
    #Asegura que exista la carpeta donde se guarda el log
    os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)
    #Se abre el archivo en modo "append" para no sobrescribir, y se escribe el log
    with open(RUTA_LOG, "a", encoding="utf-8") as archivo:
        archivo.write(linea)
        