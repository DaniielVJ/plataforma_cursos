from django.db import models
from .course import Course
# nuestro propio campo
from apps.courses.fields import OrderField


# Modelo para almacenar las secciones que tendra cada curso
class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # Define que orden tiene dentro de un grupo cada objeto de este modelo
    order = OrderField(['course'])
    
    def __str__(self):
        return f"{self.course} --> {self.title}"
    