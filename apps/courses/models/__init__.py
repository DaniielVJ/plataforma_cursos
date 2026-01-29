# Debemos evitar el error de importacion circular, para eso al momento en que se ejecutan
# estas importaciones en este mismo orden debemos tener cuidado que 2 modulos distintos
# se llamen entre si al mismo tiempo.
from .category import Category
from .section import Section
from .enrollment import Enrollment
from .progress import Progress
from .review import Review
from .course import Course, CourseCategory
from .content import Content, File, Image, Text, Video
from .progress_tracking import CompletedContent


# EJEMPLO: 
"""
🔹 Cómo funciona la importación circular en Python

Python empieza a ejecutar course.py.

Encuentra from .enrollment import Enrollment → intenta ejecutar enrollment.py.

Dentro de enrollment.py, ve from .course import Course → intenta ejecutar course.py.

Python ya está ejecutando course.py, pero todavía no ha terminado de definir Course.

Entonces Course no existe aún en memoria.

Resultado: ImportError: cannot import name 'Course' from partially initialized module.

"""