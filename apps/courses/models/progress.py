from django.db import models
from django.conf import settings
from .course import Course

# Cada objeto o registro del modelo progress sera para almacenar el progreso de un usuario en un curso
class Progress(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    update_at = models.DateTimeField(auto_now=True)
    progress = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user} - {self.course} ({self.progress})({self.status})"
    
    # Podriamos definir los metodos que queramos o funcionalidades ya que es una clase de python
    # igual que siempre, solo que hereda de Model y eso le da poderes para representar una tabla
    # aparte de crear objetos, pero si queremos proteger por ejemplo nuestros atributos podemos usar
    # property o incluso si queremos que puedan operarse como sumas, etc. method magic.
    
    class Meta:
        # Un usuario no puede tener mas de un progreso por curso
        unique_together = ('course', 'user')
        

