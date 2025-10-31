from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Ruta principal para incluir y acceder a todas las urls de la app courses
    path('courses/', include('apps.courses.urls')),
    # Rutas principales para acceder a las urls de las demas aplicaciones
    path('profile/', include('apps.profiles.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
]

