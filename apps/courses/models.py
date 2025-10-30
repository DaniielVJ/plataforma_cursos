# Al cargarlo en nuestro archivo models y al ser publicos el sistema de migracion
# podra leer las importaciones y podra implementar nuestros modelos y hacerles seguimiento
from .models.category import Category
from .models.course import Course, CourseCategory
from .models.section import Section # cargarlo aqui hara que django ahora le haga seguimiento a este modelo
from .models.enrollment import Enrollment
from .models.progress import Progress

# django ira exportando cada import de forma independiente gracias al importarlo en __init__.py

