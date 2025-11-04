import secrets
from django.db import models, IntegrityError
from django.utils.text import slugify

class AutomaticSlugField(models.SlugField):
    def __init__(self, fields=None ,*args, **kwargs):
        self.fields = fields
        super().__init__(*args, **kwargs)


    def pre_save(self, model_instance, add):
        
        if not getattr(model_instance, self.attname):
            fields_values = " ".join([getattr(model_instance, field)  for field in self.fields])
            slug = slugify(fields_values)
            query = {self.attname: slug}
            
            attempt = 1
            while self.model.objects.filter(**query).exists() and attempt <= 5:
                slug +=  secrets.token_hex(3)
                query[self.attname] = slug
                attempt += 1
            
            if attempt > 5:
                raise IntegrityError("EL VALOR DEBE SER UNICO")
            
            setattr(model_instance, self.attname, slug)
            return slug
        return super().pre_save(model_instance, add)



