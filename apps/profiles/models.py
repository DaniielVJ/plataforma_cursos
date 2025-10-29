# Mandamos a llamar nuestros modelos - Ya que este el archivo que django lee para cargar los modelos
# y hacer seguimiento


# Al importar ya carga todo el codigo de esos archivos aqui, como si hubieran
# sidos creados aqui para ser utilizados.
from .models.user import User
from .models.instructor import Instructor

# A traves del init podremos cargar nuestros modelos aqui para que django los siga
# ya que este dice que deben cargarse al importar de (from) de ese paquete en el archivo
# que los necesite y en ese mismo orden si tienen dependencia entre si.

# ESTO ES DIFERENTE DE UNA IMPORTANCION NORMAL, PORQUE HACE IMPORTABLE LOS MODELOS
# DE OTROS ARCHIVO, AHORA YO PODRIA IMPORTARLOS DE ESTE ARCHIVO EN OTRO ARCHIVO
# LITERAL LOS CARGA COMO SI SE INICILIZARAN O DEFINIERAN AQUI MISMO

