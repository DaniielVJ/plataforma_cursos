from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class OrderField(models.PositiveIntegerField):
    
    def __init__(self, for_fields, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)
        
        
    def pre_save(self, model_instance, add):
        try:
            if getattr(model_instance, self.attname) is None:
                qs = self.model.objects.all()
                
                if self.for_fields:
                    # construir condicion de filtrado
                    query = { field:getattr(model_instance, field) for field in self.for_fields}

                    # desempaquetamos el diccionario en keywordarguments para usarlos como condicion de filter
                    qs = qs.filter(**query)
                    
                    # Obtenemos al objeto con el valor mas alto en ese campo del grupo o queryset
                    last_item = qs.latest(self.attname)
                    
                    # value es igual al que tiene ese objeto en el campo orderfield + 1
                    value = getattr(last_item, self.attname) + 1 
                    
                    # antes de guardar el objeto en la base de datos para su campo orderfield
                    # le asignamos ese valor.
                    setattr(model_instance, self.attname, value)    
        
        except ObjectDoesNotExist:
            value = 0            
        return super().pre_save(model_instance, add)