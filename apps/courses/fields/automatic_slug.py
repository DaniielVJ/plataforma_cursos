# Modulo estandar que permite generar tokens aleatorios
import secrets
from django.db import models, IntegrityError
# funcion que recibe un texto o string en cualquier formato y lo pasa a formato slug
from django.utils.text import slugify

# Definimos la clase que nos permitira crear un campo, donde un field o campo es un objeto
# asociado a un atributo, donde la clase define como se comportara el campo objeto.
class AutomaticSlugField(models.SlugField):
    def __init__(self, fields=None ,*args, **kwargs):
        self.fields = fields
        super().__init__(*args, **kwargs)


    # Los constraint como UNIQUE, se evaluan antes del metodo pre_save, asi que si hay una excepción, puede
    # que sea un constraint definido, y no nuestro metodo pre_save.
    def pre_save(self, model_instance, add):
        
        if not getattr(model_instance, self.attname):
            fields_values = " ".join([getattr(model_instance, field)  for field in self.fields])
            slug = slugify(fields_values)
            
            # slug repetido para probar que funcione
            # slug = "estructuras-de-datos536c75"
            query = {self.attname: slug}
            
            attempt = 1
            while self.model.objects.filter(**query).exists() and attempt <= 5:
                slug +=  secrets.token_hex(3)
                query[self.attname] = slug
                attempt += 1
            
            if attempt > 5:
                raise IntegrityError("EL VALOR DEBE SER UNICO ESE SLUG EXISTE")
            
            setattr(model_instance, self.attname, slug)
            return slug            
        return super().pre_save(model_instance, add)



