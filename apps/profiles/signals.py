# Modulo que creamos para definir las signals de la app "courses"

# signal que se ejecuta despues de haber guardado un objeto en los modelos
from django.db.models.signals import post_save
# recibidor de signals
from django.dispatch import receiver
from django.conf import settings
from .models import InstructorProfile 


# Definimos la funcion encargada de ejecutar la acción cuando ocurra el signal
# decoramos como receiver para darle esa funcionalidad de poder recibir o actuar
# cuando ocurra la señal, si no seria una funcion normal.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
# 1: Signal a responder
# 2: Modelo que enviara ese signal que recibiremos aqui
def create_instructor_profile(sender, instance, created, **kwargs):
    # 1: sender o modelo que envio la señal
    # 2: El objeto o instance del modelo que origino la señal
    if instance.is_instructor:
        InstructorProfile.objects.create(user=instance)
        


# pre_save: es un signal que se envia al abrir el formulario para actualizar o crear un objeto.
# post_save: es un signal que se envia al hacer click en guardar un nuevo objeto del formulario o actualizarlo.
# created: Indica si se creo el objeto(True) o se actualizo(False) originario de la señal.


#  Cualquier modulo que creemos para definir cosas y tener el codigo organizado que no sea un modulo
# que se crea en django por defecto al momento de crear una app o proyecto. Debemos importarlo o si django
# nos permite, registrarlo en uno de los modulos por defecto de django. ASI QUE LOS SIGNALS debemos registrarlos
# en apps.py de la aplicacion a la cual pertenescan
