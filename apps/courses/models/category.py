from django.db import models


# Modelo para almacenar cada categoria que puede tener un curso
# una categoria podria asociarse a muchos cursos
class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    # Es para que cada categoria tenga una forma unica para ser buscado en la url
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
