# Modelo para almacenar el progreso de un estudiante en un curso
from django.db import models
from django.conf import settings
from .content import Content


class CompletedContent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="completed_content")
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    

    # Usamos una clase anidada para definir los atributos que son configuraciones, para diferenciarlo
    # de los atributos de la clase que indican que seran un campo del modelo.
    class Meta:
        # Estos 2 campos deben ser unicos por registro del modelo
        unique_together = ('user', 'content') # Un usuario no puede completar el mismo contenido dos veces
        



