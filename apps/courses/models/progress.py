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

    
    class Meta:
        # Un usuario no puede tener mas de un progreso por curso
        unique_together = ('course', 'user')
        

    def __str__(self):
        return f"{self.user} - {self.course} ({self.progress})({self.status})"