from django.db import models
# Esta tabla o modelo asocia la app a sus modelos
from django.contrib.contenttypes.models import ContentType
# Este campo permite asociar a un objeto de un modelo en especifico.
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from .section import Section
from apps.courses.fields import OrderField

# Modelo padre para nuestro modelo polimorfico.
class ItemBase(models.Model):
    # usado para heredar campos comunes a otros modelos
    
    # Asociamos cada item creado a un propietario o usuario que lo creo
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_related")
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    # Este modelo no crea tabla
    class Meta:
        abstract = True

    def __str__(self):
        return self.title
    

# Modelos hijos heredan o implementan todos los campos y metodos del modelo Padre
# Simplemente debemos añadir los campos propios de los diferentes modelos hijos
class Text(ItemBase):
    content = models.TextField()
    
# Para cada modelo hijo se crea una tabla 
class File(ItemBase):
    file = models.FileField(upload_to='files/')


class Image(ItemBase):
    file = models.FileField(upload_to='images/')


class Video(ItemBase):
    url = models.URLField()


# Modelo para almacenar el contenido o leccion de cada sección de un curso en especifico
class Content(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="contents")
    # Esto asocia el content a un tipo de contenido, ya que puede ser un articulo, un video, imagen, etc..
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={
        # Aqui se especifica a que modelos puede estar asociado cada objeto de content
        'model__in': ('text', 'file', 'image', 'video')
    })
    # contiene el identificador del recurso o objeto del modelo al que se asocie en el campo content_type
    object_id = models.PositiveIntegerField()
    # Item es el campo que realmente almacenara el contenido de cada registro content, la imagen, articulo, video, etc.
    # Entonces este campo permite asociar ese item o recurso a un tipo de contenido que es.
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(['section'])
    
    


# content_type: este campo indica a que modelo esta asociado cada objeto de el modelo content igual que cualquier otro
# la unica diferencia es que el modelo puedo variar entre objetos de content.

# object_id: contien el id del objeto del modelo content_type al cual este asociado el content.

# item: Este campo es el encargado de asociar cada objeto de content con el objeto del modelo al cual 
# este asociado el content en el campo content_type.

# Implementar Modelo polimorfico: Modelo Content sus objetos pueden agarrar multiples formas (video, imagen, documento)
# por lo tanto es un Modelo polimorfico.
