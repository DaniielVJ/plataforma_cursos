from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.profiles'


    # Se ejecuta cuando django termina de cargar la app y esta lista para funcionar o ready
    def ready(self):
        # Cargamos o ejecutamos los signals de la app
        import apps.profiles.signals
        
        # Aqui al poner importaciones, el codigo de estas se ejecutara al momento de 
        # que la app este lista o ejecutandose ya el sistema. al importar un modulo
        # se ejecuta todo su codigo y el decorador @reciever es el encargado al momento
        # que es ejecutado por que este modulo lo importo, de registrar la funcion
        # en django para que escuche las señales que se le programo
        