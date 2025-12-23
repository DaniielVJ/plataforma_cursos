from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Ruta principal para incluir y acceder a todas las urls de la app courses
    # path('courses/', include('apps.courses.urls')),
    # Rutas principales para acceder a las urls de las demas aplicaciones
    path('profile/', include('apps.profiles.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('instructor/', include('apps.courses.urls.instructor')),
    path('student/', include('apps.courses.urls.student')),
]

