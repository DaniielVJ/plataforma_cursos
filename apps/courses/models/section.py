from django.db import models
from .course import Course


# Modelo para almacenar las secciones que tendra cada curso
class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    