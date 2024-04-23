# PyMangaReader
Lector de manga básico en python, con interfaz gráfica y algunas opciones interesantes.

Accesos directos 
 Flecha arriba - zoom in (tambien con el scroll del raton)
 Flecha abajo - zoom out (tambien con el scroll del raton)
 Flecha izquierda - imagen anterior
 Flecha derecha - imagen siguiente
 R - Redimensionar al tamaño actual de la ventana

· En la carpeta donde queiras guardar tu proyecto:
git clone https://github.com/salocinmad/PyMangaReader

· Creamos un entorno virtual en el sistema
python -m venv venv

Para crear un entorno virtual en Python, puedes usar el módulo `venv` que viene incorporado en Python 3.3 y versiones posteriores. Aquí están los pasos para crear un entorno virtual llamado `venv`:

1. Abre la terminal en Visual Studio Code.
2. Navega al directorio donde deseas crear el entorno virtual. Puedes usar el comando `cd` para cambiar de directorio.
3. Ejecuta el siguiente comando para crear un entorno virtual llamado `venv`:

```bash
python -m venv venv
```

Este comando crea un directorio llamado `venv` (o el nombre que elijas) en tu directorio actual. Dentro de este directorio, se instalará una copia local de Python y pip, que puedes usar para instalar paquetes de manera aislada del sistema Python global.

Para activar un entorno virtual en PowerShell, es posible que necesites cambiar la política de ejecución para permitir la ejecución de scripts. Puedes hacerlo con el comando Set-ExecutionPolicy.

Aquí está el comando que necesitas ejecutar:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Para activar el entorno virtual, usa el siguiente comando:

En Windows:

```bash
.\venv\Scripts\activate
```

En Unix o MacOS:

```bash
source venv/bin/activate
```

Una vez que el entorno virtual está activado, puedes instalar paquetes/dependencias en él usando pip. Estos paquetes estarán disponibles solo dentro de este entorno virtual y no afectarán tu instalación global de Python.

```bash
pip install rarfile pillow pdf2image
```

Ejecuta PyMangaReader en el entorno virtual.

```bash
py PyMangaReader.py
```
