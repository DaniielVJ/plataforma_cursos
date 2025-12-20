from django.db import models
from .course import Course
# nuestro propio campo
from ..fields import OrderField


# Modelo para almacenar las secciones que tendra cada curso
class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # Define que orden tiene dentro de un grupo cada objeto de este modelo
    order = OrderField(('course', ), blank=True)
    
    
    def __str__(self):
        return f"{self.title}"
    
    
    @property
    def model_name(self):
        return self._meta.model_name