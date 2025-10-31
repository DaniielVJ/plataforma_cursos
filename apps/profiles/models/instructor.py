from django.db import models
from django.conf import settings
# from django.contrib.auth import get_user_model - Se usa en views, signals y templates.


# Modelo que utilizamos para almacenar datos adicionales de los Usuarios si fuesen 
# un instructor
class InstructorProfile(models.Model):
    # Campo permite asociar un perfil de instructor a un usuario y asi aparte de ser un usuario tener perfil de instructor
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor')
    # blank - opcional para el usuario agregar eso en el formulario
    bio = models.TextField(blank=True)
    photo = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    social_network = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"Instructor: {self.user.get_full_name() or self.user.username}"
    
    