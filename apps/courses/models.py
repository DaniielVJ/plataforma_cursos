# Al cargarlo en nuestro archivo models y al ser publicos el sistema de migracion
# podra leer las importaciones y podra implementar nuestros modelos y hacerles seguimiento
from .models.category import Category
from .models.course import Course, CourseCategory
# django ira exportando cada import de forma independiente gracias al importarlo en __init__.py

