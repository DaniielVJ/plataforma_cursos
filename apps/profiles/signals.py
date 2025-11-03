# Modulo que creamos para definir los receptores de la app "profiles"

# Traemos un signal por defecto que se emite cada vez que se crea o actualiza
# un objeto de un modelo
from django.db.models.signals import post_save
# decorador que permite definir un receptor de algun signal que se emita.
from django.dispatch import receiver
from django.conf import settings
from .models import InstructorProfile 



# Implementamos el decorador receiver para darle la funcionalidad a la funcion de poder recibir o actuar
# cuando ocurra un signal, si no seria una funcion normal.

# 1: Signal a responder
# 2: Modelo que enviara ese signal que recibiremos aqui
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
# Definimos la funcion encargada de ejecutar la acción cuando ocurra el signal
def create_instructor_profile(sender, instance, created, **kwargs):
    # 1: sender o modelo que envio la señal
    # 2: El objeto o instancia del modelo que origino la señal
    if instance.is_instructor:
        InstructorProfile.objects.get_or_create(user=instance)
    else:
        InstructorProfile.objects.filter(user=instance).delete()
 
    

# pre_save: es un signal que se envia al abrir el formulario para actualizar o crear un objeto.
# post_save: es un signal que se envia al hacer click en guardar un nuevo objeto del formulario o actualizarlo.
# created: Indica si se creo(True) o actualizo(False) el objeto que origino el signal.


#  Cualquier modulo que creemos para definir cosas y tener el codigo más organizado que no sea un modulo
# que se crea en django por defecto al momento de crear una app o proyecto.debemos, 
# importarlos o registrarlo en uno de los modulos por defecto de django. ASI QUE LOS RECEPTORES debemos registrarlos
# en apps.py de la aplicacion a la cual pertenezcan ya que al ser un modulo creado por defecto por django
# 
