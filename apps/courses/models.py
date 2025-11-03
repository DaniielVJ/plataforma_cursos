# Al cargarlo en nuestro archivo models y al ser publicos el sistema de migracion
# podra leer las importaciones y podra implementar nuestros modelos y hacerles seguimiento



# Importamos y cargamos todos los modelos en el models.py para que sean visibles por django y pueda
# aplicar las migraciones de nuestro sistema.
from .models.category import Category
from .models.course import Course, CourseCategory
from .models.section import Section # cargarlo aqui hara que django ahora le haga seguimiento a este modelo
from .models.enrollment import Enrollment
from .models.progress import Progress
from .models.review import Review
from .models.content import Content, File, Image, Text, Video



# django ira exportando cada import de forma independiente gracias al importarlo en __init__.py

# Todas estas importaciones podran ser reeimportadas por django, es decir podra importar importaciones de un archivo
# ya que son publicas y llevarla al archivo de migraciones para hacer seguimiento y aplicar los cambios
# en la base de datos