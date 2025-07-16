# 📋 Registro de Stock por Categorías

Este programa permite registrar el stock de productos en un almacén, organizados en cuatro categorías principales:

- Alimentos
- Productos de limpieza
- Bebidas y lácteos
- Otros

El sistema permite agregar, editar, eliminar productos y visualizar avisos por vencimiento o bajo stock. Toda la información se guarda en un archivo `.json`, y cada acción del usuario se registra en un archivo `.log` para tener un historial completo.

---

## 🚀 Funcionalidades

- Menú interactivo usando `questionary`
- Control por **categoría**
- Avisos por vencimiento próximo o bajo stock.
- Registro automático de:
  - Entradas
  - Modificaciones
- Archivos utilizados:
  - `stock.json`: almacena el stock actual
  - `registro.log`: historial de acciones.

---

## ⚙️ Requisitos

- Python 3.10 o superior

---

## 📦 Instalación con entorno virtual

Se recomienda ejecutar el programa en un entorno virtual para mantener aisladas las dependencias del proyecto.

### 1. Crear y activar entorno virtual:

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual en Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

### 2. Instalar las librerias:

Instalación rápida:

```bash
pip install -r requirements.txt
```
---

## 📁 Archivos del proyecto
```
proyecto/
│
├── main.py               # Menú principal del programa
├── funciones/
│   ├── stock.py          # Gestión del inventario
│   ├── archivos.py       # Lectura y escritura de archivos
│   ├── menu.py           # Menús interactivos
│   └── helpers.py        # Funciones utilitarias
│
├── data/
│   ├── stock.json        # Inventario
│   └── registro.log      # Historial de movimientos
│
├── README.md             # Documentación del proyecto
└── requirements.txt      # Librerías necesarias
```
---

## 👩‍💻 Desarrollado por

Micaela Pastor  
Trabajo Final - Materia: Programación 1  
Carrera: Tecnicatura en Ciencia de Datos Julio 2025
