# Un mixin es una clase creada o pensada para simplemente añadir una funcionalidad en concreto a otra clase
# o clases que hereden de esta. No es pensada para la herencia clasica, pero se aprovecha de esta para reutilizar funcionalidades
# en concreto como las funciones pero aplicado a las clases.

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from ..models import Course

# mixing se encarga simplemente de consultar si el que quiere ejecutar la funcionalidad es un instructor
class InstructorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    # Este metodo lo sobrescribimos de UserPassesTestMixin, que lo que hace es que si retorna True
    # se ejecutan las funcionalidades de la clase, si no no se ejecutan.
    def test_func(self):
        return self.request.user.is_instructor


# Nuestro mixin implementa la funcionalidad que para ejecutarse debe el usuario estar autenticado y ademas extiende
# que debe ser instructor

class CourseListView(InstructorRequiredMixin, ListView):
    model = Course
    template_name = "instructor/list_courses.html"
    context_object_name = "courses"
    paginate_by = 8


    # retorna un queryset, con todos los cursos asociados al usuario que mando el request a esta view
    def get_queryset(self):
        return self.model.objects.select_related('owner').filter(owner=self.request.user)


