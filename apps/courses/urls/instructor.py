# modulo o archivo, para exponer todas las urls que tiene disponible un instructor dentro de la aplicacion
# de cursos.

from django.urls import path
from ..views import instructor


# app_name, es nada mas que un label que usamos como prefijo para referenciar a una url que queremos mandar a llamar
# de alguna parte de nuestro programa por su nombre. Este label permite que si en un proyecto completo de django existe
# mas de una url con el mismo nombre en otra aplicacion o archivo de python, poder diferenciarlas.

app_name = "instructor" # las urls de este archivo seran referenciadas con ese prefijo


# urls que exponen las funcionalidades
urlpatterns = [
     path('courses/', instructor.CourseListView.as_view(), name='list_courses'),
     path('course/create/', instructor.CourseCreateView.as_view(), name='create_course'),
     path('course/<str:slug>/update/', instructor.CourseUpdateView.as_view(), name='update_course'),
     path('course/<str:slug>/delete/', instructor.CourseDeleteView.as_view(), name="delete_course"),
     path('course/<str:course_slug>/sections/', instructor.SectionListView.as_view(), name="list_sections"),
     path('course/<str:course_slug>/section/create', instructor.SectionCreateView.as_view(), name="create_section"),
     path('course/<str:course_slug>/section/<int:pk>/update', instructor.SectionUpdateView.as_view(), name="update_section")
]



# el app name es por include EJ: include('modulo_con_variable_urlpatterns', app_name), esto indica que todas las urls que vincula
# ese include a una principal podran ser accesibles con su app_name seguido de el name