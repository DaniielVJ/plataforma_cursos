# Importamos la plantilla del usuario de django para reutilizarla para nuestro modelo
from django.contrib.auth.models import AbstractUser
from django.db import models



# Creamos nuestro propio modelo Users, pero a partir del que trae django
class User(AbstractUser):
    # Simplemente añadimos los campos adicionales que queremos 
    is_instructor = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.get_full_name() or self.username
    
    