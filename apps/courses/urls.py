from django.urls import path
from . import views


# Por recomendacion, darle como nombre a la ruta el mismo de la vista
urlpatterns = [
   
]





'''

Pensar en las urls por la accion que haran, en este caso como le doy el nombre
courses_list al usarla en el template yo solo puedo pensar y decir aqui pondre la url
courses_list ya que la accion que realiza es listar los cursos.

Entonces al crear una url debemos pensar que funcion hara cuando se utilize, ejemplo create_course
y al utilizar esa url es para crear el curso.

O pensar, quiero hacer esta funcionalidad, por ende voy a crear esta url y esta sera encargada de 
ejecutar dicha funcionalidad.
'''
