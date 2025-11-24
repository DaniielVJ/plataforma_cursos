from django.contrib import admin
from .models import (Category, Course, CourseCategory, 
                     Enrollment, Progress, Review, Section, 
                     File, Video, Text, Image, Content)



# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Define que el campo slug se va autocompletar automaticamente con el valor del campo name en el formulario
    # del admin.
    prepopulated_fields = {"slug": ('name',)}
    list_display = ('name', 'slug')
    search_fields = ('slug',)


class CourseCategoryInline(admin.TabularInline):
    model = CourseCategory
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'create_at']
    search_fields = ('title', 'owner__username', 'owner__first_name')
    list_filter = ('create_at', 'owner__username', 'categories__name')
    date_hierarchy = 'create_at'
    ordering = ('-create_at',)
    prepopulated_fields = {"slug": ('title', )}
    inlines = (CourseCategoryInline, )
    
    
@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('course', 'category')
    list_filter = ('category__name', )
    search_fields = ('course__title', 'category__name')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('course__title', 'title')
    

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrollment_at')
    list_filter = ('enrollment_at', )
    date_hierarchy = 'enrollment_at'
    ordering = ('-enrollment_at', )
    search_fields = ('course__title', 'user__username', 'user__first_name')


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'progress', 'status', 'update_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'course__title')
        



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'course__title')
    
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('section__course__title', 'section__title', 'item', 'section__course__owner__username')
    list_filter = ('section', )



admin.site.register(Video)
admin.site.register(File)
admin.site.register(Image)
admin.site.register(Text)