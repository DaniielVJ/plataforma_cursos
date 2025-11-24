from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, InstructorProfile
from apps.courses.models import Course


# Es crear un formulario de un modelo, para incrustarlo en el formulario
# de objeto de otro modelo.
class InstructorProfileInline(admin.StackedInline):
    model = InstructorProfile
    extra = 0


class CourseInline(admin.TabularInline):
    model = Course
    extra = 1



# permite registrar el modelo y ademas decorar una clase para que funciona como la personalizacion del modelo registrado
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Reutilizamos las configuraciones del admin del usuario de django para nuestro usuario que extiende de el
    
    # fieldsets, este atributo es para añadir fieldsets al formulario de modificar un objeto existente del modelo
    fieldsets = BaseUserAdmin.fieldsets + (('Rol personalizado', {'fields': ('is_instructor',)}), )
    
    # Este es para añadir fieldsets al formulario de añadir un nuevo objeto en un modelo   
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {"fields": ('is_instructor', )}),
    )

    list_display = BaseUserAdmin.list_display + ('is_instructor',)
    
    inlines = BaseUserAdmin.inlines + (InstructorProfileInline, CourseInline)
    

# Una clase modelAdmin aplica estas personalizaciones a cualquier modelo que se la asociemos en el django admin
# Pero se suele crear una por Modelo en especifico, porque podriamos listar campos que otro modelo no tiene, etc.
# entonces por convencion la clase tiene el nombre del modelo al cual administra en el admin.
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'user__last_login')
    




admin.site.register(InstructorProfile, InstructorAdmin)

 