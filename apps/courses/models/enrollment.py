from django.db import models
from django.conf import settings
from .course import Course

# Modelo que se encarga de almacenar el enrolamiento o inscripcion de un usuario estudiante
# a un curso en especifico. tabla intermedia que aparte de almacenar la asociacion 
# almacena la fecha en que se hizo esa asociacion, o en logica de negocio de este sistema
# la fecha en que el estudiante se inscribio en el curso
class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrollment_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Inscripción de {self.user} a {self.course}"
    
    class Meta:
        unique_together = ('user', 'course')
        
        