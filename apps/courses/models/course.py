from django.db import models
from django.conf import settings
from .category import Category
from ..fields import AutomaticSlugField

# Modelo que almacena cada curso que tendra el sistema
class Course(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_courses")
    title = models.CharField(max_length=200)
    # Nombre propio que tendra cada curso para ser buscado por la url
    slug = AutomaticSlugField(fields=['title'])
    overview = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name="courses", through="CourseCategory")
    # Para acceder a los cursos que es propietario el usuario usara owned_courses y los que no es propietario courses
    # students = models.ManyToManyField(settings.AUTH_USER_MODEL, through=Enrollment, related_name='courses')
    # ESTO PARA QUE FUNCIONE HAY QUE USAR STRING O DEFINIR LA TABLA INTERMEDIA EN EL MISMO ARCHIVO
    
    
    class Meta:
        # ordering en el modelo, es para definir en que orden seran devueltos los objetos de este modelo
        # al consultarlos.
        ordering = ('-create_at', )
         
    def __str__(self):
        return self.title
    
   
   
# En este caso  la relacion muchos a muchos no tiene campos adicionales asi que no habria justificacion de que
# nosotros creemos la tabla intermedia, podria crearla django, pero si deseamos personalizarla para el django admin
# debemos crearla manualmente.
class CourseCategory(models.Model):
    # on_delete, tabla intermedia permite que si se elimina una categoria o un curso  se elimen todas las relaciones
    # que tenia una categoria con ese curso eliminado por ejemplo y viceversa. Sin eliminar a la categoria solo la relacion
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


    class Meta:
        # Permite que un registro de un modelo no pueda asociarse mas de una vez con
        # el mismo registro de otro modelo, sino que cada asociacion debe ser con un registro
        # distinto
        unique_together = ("course", "category")
        
    def __str__(self):
        return f"{self.course} ----> {self.category}"