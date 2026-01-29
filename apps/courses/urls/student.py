# En este modulo definiremos las urls que expondremos o podran utilizar los estudiantes
from django.urls import path
from ..views import student

app_name = "student" # las urls de este archivo seran referenciadas con ese prefijo


urlpatterns = [
    path('courses/', student.courses_list, name='courses_list'), # /courses -> listar los cursos
    path('courses/detail/<str:slug>', student.course_detail, name='course_detail'), # mostrar detalles del curso
    # Lo que estamos diciendo es que el valor que se mande en esa parte del path lo pasaremos al parametro slug de la view 
    path('courses/<str:slug>/lessons/', student.course_lessons, name='course_lessons') # url para mostrar la leccion del curso seleccionada
]