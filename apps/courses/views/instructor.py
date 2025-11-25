# Un mixin es una clase creada o pensada para simplemente añadir una funcionalidad en concreto a otra clase
# o clases que hereden de esta. No es pensada para la herencia clasica, pero se aprovecha de esta para reutilizar funcionalidades
# en concreto como las funciones pero aplicado a las clases.

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
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



class CourseCreateView(InstructorRequiredMixin, CreateView):
    model = Course
    # CreateView hereda de ModelFormMixin, que este evalua que si el campo fields esta vacio usa como formulario el que
    # pasemos en form_class y ese sera el formulario que usara para crear un objeto y se basara en sus configuraciones.
    # Pero si nosotros pasamos a fields una lista con los campos que especifiquemos, esta automaticamente si no indicamos 
    # form_class crea el formulario necesario para recibir solo esos valores que indicamos y validarlos para que pueda
    # aceptarlos el modelo sin ningun problema.

    # Por lo tanto si no necesitamos hacer validaciones personalizadas como validar un password tenga mayusculas, minusculas,
    # etc. podemos permitir que django la clase cree el formulario para recibir los datos de los campos que especifiquemos
    # ya que recordemos que en un formulario solo se le crean los campos que queremos obtener por parte del usuario
    # e inclusive en el modelo configuramos si seran obligatorios en el formulario o no, el formulario solo valida los campos
    # que se le definen si es Form y si es modelForm solo los que se envian al usuario especificado con fields=[] y exclude=[]
    # con fields de la View podemos especificar que campos debe validar si o si porque provienen de un usuario y puede
    # mandar cualquier custion. luego que esos datos sean validados por .is_valid el formulario crea una instancia del modelo
    # y la almacena en .instance y ahi podemos asociarle o asignarles los datos que nuestra app debe proveer no el usuario

    fields = [
        'title', 'slug', 'overview', 
        'image', 'level', 'content_duration',
        'categories'
    ] # campos que el formulario recibira datos del usuario, no necesitamos un form_class pq los datos que envia el 
    # el usuario no requieren logica personalizada
    
    template_name = "instructor/form_course.html"
    success_url = reverse_lazy('instructor:list_courses')

    # Logica si el formulario con los datos que definimos que debe aceptar del usuario, todos esos datos estan validos
    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)
    


# View que permite actualizar el curso que se solicite en la url dinamica a traves de su slug
class CourseUpdateView(InstructorRequiredMixin, UpdateView):
    model = Course
    fields = [
        'title', 'slug', 'overview', 
        'image', 'level', 'content_duration',
        'categories'] 
    template_name = "instructor/form_course.html"
    success_url = reverse_lazy('instructor:list_courses')
    # Con que nombre debe buscar el slug dentro del path dinamico de la url
    slug_url_kwarg = 'slug'
    # El nombre del campo slug del modelo donde debe ir a buscar el slug enviado por la url
    # y si existe traer la instancia y devolverla en el formulario para ser actualizada
    slug_field = 'slug'

    def get_queryset(self):
        
        return self.model.objects.filter(owner=self.request.user)


class CourseDeleteView(InstructorRequiredMixin, DeleteView):
    model = Course
    template_name = 'instructor/delete_course.html'
    success_url = reverse_lazy('instructor:list_courses')
    slug_field = "slug"
    slug_url_kwarg = "slug"


    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    

    