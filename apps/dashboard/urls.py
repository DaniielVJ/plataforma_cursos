from django.urls import path
from . import views



urlpatterns = [
    # raiz de dashboard, es decir usa la ruta definida en el proyecto para dashboard
    path('', views.index, name='dashboard_index') # responde a -> /dashboard
    # <- url encargada de cargar el index de dashboard
]
