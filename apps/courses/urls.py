from django.urls import path
from . import views


# Por recomendacion, darle como nombre a la ruta el mismo de la vista
urlpatterns = [
    path('', views.courses_list, name='courses_list'), # /courses -> listar los cursos
    path('detail/', views.course_detail, name='course_detail'), # mostrar detalles del curso
    path('lessons/', views.course_lessons, name='course_lessons') # url para mostrar la leccion del curso seleccionada
]





'''

Pensar en las urls por la accion que haran, en este caso como le doy el nombre
courses_list al usarla en el template yo solo puedo pensar y decir aqui pondre la url
courses_list ya que la accion que realiza es listar los cursos.

Entonces al crear una url debemos pensar que funcion hara cuando se utilize, ejemplo create_course
y al utilizar esa url es para crear el curso.

'''
