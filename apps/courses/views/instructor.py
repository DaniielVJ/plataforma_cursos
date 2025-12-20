# Un mixin es una clase creada o pensada para simplemente añadir una funcionalidad en concreto a otra clase
# o clases que hereden de esta. No es pensada para la herencia clasica, pero se aprovecha de esta para reutilizar funcionalidades
# en concreto como las funciones pero aplicado a las clases.

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.forms.models import modelform_factory
from django.contrib.contenttypes.models import ContentType


from ..models import Course, Section, Content, Text, Video, File, Image


# Diccionario que referencia a los Modelos a los cual puede pertenecer un contenido
CONTENT_MODELS = {
    "video": Video,
    "file": File,
    "text": Text,
    "image": Image,
}



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
    template_name = 'instructor/confirm_course_delete.html'
    success_url = reverse_lazy('instructor:list_courses')
    slug_field = "slug"
    slug_url_kwarg = "slug"


    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    

# Section Views

class SectionListView(InstructorRequiredMixin, ListView):
    model = Section
    template_name = "instructor/list_sections.html"
    context_object_name = "sections"
    

    # Devuelve solo las secciones asociadas a un curso que tenga como propietario al usuario que envio el request
    # a esta view
    def get_queryset(self):
        # self.kwargs: atributo que se define a todas las views genericas de django para almacenar los valores que se mandan
        # en el path de la url. solo hay que especificar el keyword con el que se identificaran los valores en el path
        self.course = get_object_or_404(Course, slug=self.kwargs['course_slug'], owner=self.request.user)
        return self.course.sections.prefetch_related('contents').order_by('order')

    
    # Define que datos del context de la View seran enviados al Context del template para ser renderizados
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context



class SectionCreateView(InstructorRequiredMixin, CreateView):
    model = Section
    template_name = 'instructor/form_section.html'
    fields = ['title', 'description']
    
    def form_valid(self, form):
        self.course = get_object_or_404(Course, slug=self.kwargs['course_slug'], owner=self.request.user)
        form.instance.course = self.course
        return super().form_valid(form)
    
    

    def get_success_url(self):
        return reverse('instructor:list_sections', kwargs={'course_slug': self.kwargs.get('course_slug')})
    


class SectionUpdateView(InstructorRequiredMixin, UpdateView):
    model = Section
    fields = ['title', 'description']
    template_name = 'instructor/form_section.html'
   
    def get_queryset(self):
        # que busque el objeto o la sección que tenga el pk que se envia por la url solo dentro de este queryset
        return self.model.objects.filter(course__slug=self.kwargs['course_slug'], course__owner=self.request.user)
   

    def get_success_url(self):
        return reverse('instructor:list_sections', kwargs={'course_slug': self.kwargs['course_slug']})


class SectionDeleteView(InstructorRequiredMixin, DeleteView):
    model = Section
    template_name = "instructor/confirm_section_delete.html"

    def get_queryset(self):
        return self.model.objects.filter(course__slug=self.kwargs.get('course_slug'), course__owner=self.request.user)
    
    def get_success_url(self):
        return reverse('instructor:list_sections', kwargs={'course_slug': self.kwargs.get('course_slug')})

     
class ContentListView(InstructorRequiredMixin, ListView):
    model = Content
    template_name = "instructor/list_contents.html"

    def get_queryset(self):
        self.section = get_object_or_404(Section, pk=self.kwargs.get('section_id'), course__owner=self.request.user)
        return self.section.contents.select_related('content_type').order_by('order')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['section'] = self.section
        return context_data


# View polimorfica o generica, se llama asi debido a que permite realizar la misma operacion de crear o actualizar un registro u objeto 
# de multiples modelos a la vez, no de solo uno como lo hace cualquier CBV generic anterior.
class BaseCreateUpdateContentView(View):
    template_name = "instructor/content_form.html"

    # Este metodo se encarga de obtener el modelo por el cual se este consultando desde el navegador
    def get_model(self, model_name):
        if not model_name in CONTENT_MODELS:
            raise Http404()
        return CONTENT_MODELS.get(model_name)

    # Este metodo se encarga de construir el formulario segun el modelo o el tipo de contenido sobre el cual se desee trabajar
    def get_form(self, model, *args, **kwargs):
        # Funcion que nos ofrece django para crear o diseniar la clase un formulario de forma automatizada
        #  para obtener datos de un modelo, sin la necesidad de diseniar una clase
        Form =  modelform_factory(model, exclude=['owner', 'created_at', 'update_at'])
        # Una vez creamos el formulario le pasamos los argumentos posicionales o de palabra clave que se proporcionen en la interfaz de este metodo
        # puede ser datos con los que rellenar sus campos, archivos o de una instancia que ya existe
        return Form(*args, **kwargs)


    # Sobreescribimos el dispatch para que antes de que este defina a que metodo debe despachar o ceder el request, este determine
    # la section y el modelo sobre el cual se requiere trabajar. y si la operacion que se desea realizar es de creacion o actualizacion.
    def dispatch(self, request, section_id=None, id=None, model_name=None, *args, **kwargs):
        self.section = get_object_or_404(Section, pk=section_id, course__owner=self.request.user)
        self.model = self.get_model(model_name)
        self.object = None
        # Si id, no tiene su valor por defecto, es decir tiene valor, significa que desde el navegador se esta solicitando un objeto
        # que existe, por ende se requiere una actualizacion
        if id:
            content_type = ContentType.objects.get_for_model(self.model)
            content = get_object_or_404(Content, pk=id, content_type=content_type, section=self.section)
            self.object = content.item
        return super().dispatch(request, section_id, id, model_name, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        # obtengo la instancia del formulario y la rellenamos con los datos correspondientes, ahora si no se recibe ningun valor
        # en data, files o instance pq son None o estan vacios, los formularios en django son lo bastantemente inteligentes para crearse vacios
        # lo que significa que este get es para crear un objeto, ahora si instance tiene valor significa que es para actualizar pq existe un object
        # entonces se rellenara con los datos que tiene esta instancia en la base de datos. y se mandara el formulario con esos valores para modificarlos
        form = self.get_form(self.model, instance=self.object)
        return render(request, self.template_name, {
            'form': form,
            'object': self.object,
            'section': self.section
        })        


    def post(self, request, section_id, id, model_name, *args, **kwargs):
        # Si el metodo del request es POST se ejecutara esta funcion o metodo, que puede ejecutarse en 2 casos.
        # Para crear un objeto o actualizar uno.
        form = self.get_form(self.model, data=request.POST, files=request.FILES, instance=self.object)        
        
        if form.is_valid():
            if not id:
                instance = form.save(commit=False)
                instance.owner = request.user
                instance.save()
                Content.objects.create(section=self.section, item=instance)
                return redirect('instructor:content_list', section_id=self.section.pk, course_slug=self.section.course.slug)
            
            form.save()
            return redirect('instructor:content_list', section_id=self.section.pk, course_slug=self.section.course.slug)
        
        return render(request, self.template_name, {
            'form': form,
            'object': self.object,
            'section': self.section
        })

# Esta view es la que realmente enrutametros en urls.py para que sea la que se mande a ejecutar, ya que lo hacemos de esta forma para que
# la sobreescritura del dispatch, toda la logica que implementamos ahi, no se ejecute antes de ejecutar el dispatch del Mixin, que solicita 
# que sea un instructor y que este autenticado haciendolo mas seguro
class CreateUpdateContentView(InstructorRequiredMixin, BaseCreateUpdateContentView):
    pass



class DeleteContentView(InstructorRequiredMixin, DeleteView):
    model = Content
    template_name = 'instructor/confirm_content_delete.html'

    def get_queryset(self):
        self.section = get_object_or_404(Section, pk=self.kwargs.get('section_id'), course__owner=self.request.user)
        return self.model.objects.filter(section=self.section)
    

    def form_valid(self, form):
        self.object.item.delete()
        self.object.delete()
        return redirect('instructor:content_list', section_id=self.section.pk, course_slug=self.section.course.slug)





