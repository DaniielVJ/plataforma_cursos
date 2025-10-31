from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, InstructorProfile


# permite registrar el modelo y ademas decorar una clase para que funciona como la personalizacion del modelo registrado
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Reutilizamos las configuraciones del admin del usuario de django para nuestro usuario que extiende de el
    
    # Aqui decimos que use los fieldset que tenia para los campos del modelo User de django + fieldset
    # para los campos nuevos que le agregamos. Estos los muestra cuando abrimos el formulario de un objeto que ya esta
    # registrado en el modelo
    fieldsets = BaseUserAdmin.fieldsets + (('Rol personalizado', {'fields': ('is_instructor',)}), )
    
    # Este permite añadir los campos al formulario para añadir un nuevo objeto del Modelo    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {"fields": ('is_instructor', )}),
    )

    list_display = BaseUserAdmin.list_display + ('is_instructor',)
    
    

# Una clase modelAdmin aplica estas personalizaciones a cualquier modelo que se la asociemos en el django admin
# Pero se suele crear una por Modelo en especifico, porque podriamos listar campos que otro modelo no tiene, etc.
# entonces por convencion la clase tiene el nombre del modelo al cual administra en el admin.
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'user__last_login')
    




admin.site.register(InstructorProfile, InstructorAdmin)

 