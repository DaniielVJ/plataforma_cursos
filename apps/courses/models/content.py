from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
# Esta tabla o modelo asocia la app a sus modelos
from django.contrib.contenttypes.models import ContentType
from .section import Section


# Modelo para almacenar el contenido o leccion de cada sección de un curso en especifico
class Content(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="contents")
    # Esto asocia el content a un tipo de contenido, ya que puede ser un articulo, un video, imagen, etc..
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # contiene el id del recurso al cual esta asociado en el modelo que apunte cada objeto
    object_id = models.PositiveIntegerField()
    # Item es el campo que realmente almacenara el contenido de cada registro content, la imagen, articulo, video, etc.
    # Entonces este campo permite asociar ese item o recurso a un tipo de contenido que es.
    item = GenericForeignKey('content_type', 'object_id')

