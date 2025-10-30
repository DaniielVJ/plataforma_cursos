# El init permite que cuando se importe el paquete para usar estos modelos
# estos 2 se carguen y comuniquen entre si.

from .user import User
# PRIMERO CARGA USER Y LUEGO INSTRUCTOR PORQUE INSTRUCTOR DEPENDE DE USER
from .instructor import Instructor



# PROPOSITO 


"""
Convertir en paquete:	__init__.py le dice a Python: “esta carpeta se puede importar”
Simplificar imports:	Permite importar todo directamente desde el paquete
Controlar inicialización:	Decide qué módulos o clases se cargan al importar el paquete
Evitar importaciones circulares:	Centraliza dependencias para evitar errores de “import loop”
"""


# HACE LAS IMPORTACIONES PUBLICAS PERMITIENDO QUE AL IMPORTARLAS EN UN ARCHIVO PUEDAN SER IMPORTADAS DE ESE ARCHIVO
# AL NO IMPORTARLAS EN EL INIT SE IMPORTARIAN DE FORMA NORMAL, ES DECIR PRIVADAS SOLO EXISTIRIAN EN ESE ARCHIVO MODELS.PY
# INTERNAMENTE Y SI DJANGO NECESITA IMPORTARLAS EN SU ARCHIVO DE MIGRACIONES NO PODRA PQ NO LAS DETECTARA POR SER PRIVADAS
# PERO AL SER PUBLICAS EL ARCHIVO DE MIGRACIONES Y CUALQUIER OTRO ARCHIVO DE PYTHON PUEDE IMPORTAR LAS IMPORTACIONES DE UN 
# ARCHIVO.