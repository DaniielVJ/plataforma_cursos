from django.db import models
from django.conf import settings
from .course import Course


# Modelo para almacenar las review de un usuario sobre un curso
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    # calificacion
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)   
    
    
    def __str__(self):
        return f"Review: {self.course} - {self.user} ({self.rating}🌟)"    
    
    class Meta:
        unique_together = ('user', 'course')
        
        
