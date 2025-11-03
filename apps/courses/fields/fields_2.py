# Este modulo lo usamos para definir nuestros propios campos personalizados
# que extendien las funcionalidades de otros campos.

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# LO QUE HACE ESTE CAMPO ES DEFINIR AUTOMÁTICAMENTE EL VALOR QUE DEBE TENER UN OBJETO
# EN ESTE CAMPO. DICHO VALOR REPRESENTA SU ORDEN DENTRO DE UN GRUPO DETERMINADO.

class OrderField(models.PositiveIntegerField):
    
    # for_fields, es el campo por el cual agruparemos y llevaremos el orden
    # lo define el usuario o programador al definir un modelo con este campo.
    
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        # Traemos el constructor del padre para que defina todos los atributos
        # del padre a los objetos de nuestra clase hija
        super().__init__(*args, **kwargs)
    
    
    # Este metodo ejecuta logica sobre el objeto del modelo antes que se guarde en la tabla o base de datos
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            try:
                qs =  self.model.objects.all()

                if self.for_fields:
                    # Si mando campos por agrupar al momento de definir en el modelo un campo OrderField(for_fields=['course'])
                    # entonces aqui vamos agrupar a todos los objetos del modelo que tengan el mismo valor
                    # en los campos de agrupamiento que le estamos pasando en el atributo for_fields.
                    
                    # Es como usar un group by en base de datos agrupar a todos los objetos que tengan el mismo valor en ese campo
                    # o columna y definirles un orden interno dentro de ese grupo.
                    # Ejemplo agrupar por el campo course en section, donde todas las secciones que pertenescan a un mismo curso
                    # seran parte del mismo grupo, y dentro de ese grupo o curso le definimos un orden interno.
                    
                    # creamos un diccionario con la clave con el nombre del campo y como valor el que tiene el objeto en ese campo
                    query = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    
                    # Aqui tenemos todos los objetos agrupados. o objetos que tengan el mismo valor en ese campo
                    # ej: todas las secciones asociadas al mismo curso
                    qs = qs.filter(**query)
                    
                    # obtenemos el valor maximo que haya para la columna de orderfield para ese grupo de objetos
                    # del modelo agrupados por un valor comun.
                    last_item = qs.aggregate(max_value=models.Max(self.attname)).get('max_value')
                    
                    # Aqui evaluamos si es el primer objeto asociado a ese grupo si lo es sera el con el order en 1
                    # si no es el primero entonces obtenemos el numero mas alto que haya en esa columna para ese grupo
                    # para sumarle 1 y ahora este pase a ser el mas grande dentro de ese grupo
                    value = 1 if last_item is None else last_item  + 1
                    
                    # A la instancia o objeto que se esta almacenando en la columna orderfield de la tabla de la base de datos
                    # le establecemos como valor el calculado.
                    setattr(model_instance, self.attname, value)
                
            except ObjectDoesNotExist:
                value = 0
        
        
        # Llamamos al padre y le pasamos los valores, para que por defecto ejecute la logica
        # del pre_save del padre nuestro objeto OrderField
        return super().pre_save(model_instance, add)




# En vez de crear una clase que here directamente de un Field, que convertiria mi clase
# en un campo de django. Mejor heredamos un tipo de field ya existente. Para no tener
# que implementar sus funcionalidades desde cero. en este caso nuestro OrderField a heredar
# de PositiveIntegerField implementa todas las funcionalidades de un numero entero positivo
# mas las que nosotros definamos.



    
    
