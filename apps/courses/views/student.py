# Se pueden dividir las urls o las view por usuario que utilizara esas funcionalidades.
# o si tenemos multiples usuarios que podran ejecutar las mismas funcionalidades
# podriamos dividir o modularizar el programa por funcionalidad y no por usuarios


# shortchut que ahorra el hacer un 404 si el objeto a buscar no existe
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Case, When
from django.core.paginator import Paginator
from django.shortcuts import redirect
from ..models import Course, Enrollment, CompletedContent, Content, Progress, Section

def courses_list(request):

    courses = Course.objects.select_related('owner')

    query = request.GET.get('query')
    page_number = request.GET.get('page')

    if query:
        courses = courses.filter(
            Q(title__icontains=query) | Q(owner__first_name__icontains=query) | Q(owner__last_name__icontains=query)
            )


    # Paginador se implementa siempre despues de haber aplicado todos los filtros
    # ya que queremos dividir en paginas los resultados a mostrar
    paginator = Paginator(courses, 8)
    page_courses = paginator.get_page(page_number)

    query_params = request.GET.copy()
    
    if 'page' in query_params:
        query_params.pop('page')

    query_params = query_params.urlencode()
    
    return render(request, 'courses/courses.html', {'page_courses': page_courses, 'query': query,  'query_params': query_params})


def course_detail(request, slug):
    # debemos pasar el modelo del cual queremos obtener el unico objeto y el filtro para obtener el objeto
    # es decir que traiga el curso que su campo slug sea igual al slug enviado por el request en el path o url.
    # course = get_object_or_404(Course, slug=slug) # forma normal

    # Optimizada
    course = get_object_or_404(Course.objects
                             .select_related("owner__instructor")
                             .prefetch_related("sections__contents"), 
                             slug=slug)

    course.image = ""
    sections = course.sections.all().order_by('order')

    return render(request, 'courses/course_detail.html', {'course': course, 'sections': sections})




# View que ejecuta la logica cuando el usuario le da a continuar aprendiendo en el curso, se encarga
# de obtener el curso, las secciones y sus contenidos. para devolver un template con los contenidos que puede consumir del curso.
def course_lessons(request, slug, content_id=None):
    course = get_object_or_404(Course, slug=slug)
    course_title = course.title
    sections = course.sections.prefetch_related('contents').order_by('order')
    
    # Si no existe una enrolacion o inscripcion del usuario al curso que quiere acceder a sus lecciones
    # le creamos una enrolacion es decir que se inscribio al curso.
    # if not Enrollment.objects.filter(user=request.user, course=course).exists():
    #     Enrollment.objects.create(user=request.user, course=course)

    # Forma mas optimizada de realizar la misma tarea
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)

    # Los print imprimen info en la terminal del servidor o pc donde se ejecuta la app, sirven como un log del sistema
    print(f"{request.user.username} se ha inscrito correctamente en el curso: {course.title}" 
          if created else 
          f"{request.user.username} ya esta inscrito en el curso {course.title}")

    # Obtener todos los contenidos
    all_contents = [ content for section in sections 
                             for content in section.contents.all() ]
    total_contents = len(all_contents) 

    # Traerse todos los contenidos que ha completado el usuario para este curso.
    # values_list(): permite obtener una lista que se componga solo de los valores de los campos del objeto en vez de almacenar o tener el campo completo.
    # flat = True, le dice al metodo value_list() que si la lista se compone solo de 1 campo de los objetos del queryset, no los regrese cada uno dentro
    # de una tupla ((1,), (2, ), (3,) ...), si no que como elementos de la lista tal cual [1, 2, ,3 ...]
    completed = CompletedContent.objects.filter(user=request.user, content__in=all_contents).values_list('content__id', flat=True) 

    # marcar el progreso por seccion
    for section in sections:
        # Aqui filtramos todos los contenidos asociados a la seccion que su id se encuentre dentro de la lista de contenidos completados
        # del curso, por lo tanto nos devuelve solamente los contenidos de la seccion completados y esos los contamos cuantos registros
        # son.
        section.completed_count = section.contents.filter(id__in=completed).count()
        # related_name se convierte en un atributo, que permite acceder a los contenidos asociados a la seccion ya sea de forma filtrada o a todos con all()
        # o solo a la cuenta de todos los contenidos que tiene asociado.
        section.total_count = section.contents.count()
        section.completed = section.completed_count == section.total_count
    

    # Contenido actual, o el contenido que debe estar seleccionado y mostrarse en el template en la parte del video
    current_content = None

    if content_id:
        current_content = get_object_or_404(Content, pk=content_id, section__course=course)


    # Progreso del curso seleccionado en porcentaje
    progress = completed.count() * 100 / total_contents if total_contents else 0

    # Si no existe un progreso para el usuario en el curso solicitado creamos un progreso para ese curso al usuario, donde este nuevo
    # registro progress o objeto progress tendra como valores tanto lo de los filtros como los default. pero si existe, solo se actualizan
    # los valores o campos del objeto o progreso que se especifican en defaults.
    Progress.objects.update_or_create(user=request.user, course=course,
                                      # defaults son los valores que se actualizan si es que existe un progreso para el usuario en ese curso
                                      # que selecciono.
                                      defaults={'progress': progress, 
                                                'status': "Completado" if progress == 100 else "En curso"})




    return render(request, 'courses/course_lessons.html', 
                  { 'course_title': course_title, 
                    'sections': sections,
                    'course': course,
                    'completed_ids': set(completed),
                    'current_content': current_content,
                    'progress': int(progress)
                    }) 


# View que marca una leccion como completada
def mark_complete(request, content_id):
    content = get_object_or_404(Content.objects.prefetch_related('section__course'), pk=content_id)
    CompletedContent.objects.get_or_create(content=content, user=request.user)
    next_content = content.get_next_content()
    
    # Los objetos independiente que si no implementan __bool__, siempre seran True asi que si me regresa un objeto
    # es pq hay next_content si no, significa que el metodo regreso None, pq estamos usando .first()
    pk = next_content.pk if next_content else content.pk

    return redirect('student:course_lessons', slug=content.section.course.slug, content_id=pk)
    

    # Esta linea es solo para acordarme si necesito utilizar un render o funcionalidad otra view, para no andar redireccionando y consumir ancho banda
    # paso a la otra view altiro y el response que me regresa lo retorno.
    # return course_lessons(request, content.section.course.slug, content.pk)











# Mi primera logica antes de refactorizar y darme cuenta que podia mejorarlo un monton (1 mes y 10 dias sin tocar django, re oxidado andaba)

# View que marca una leccion como completada
# def mark_complete(request, content_id):
#     content = get_object_or_404(Content.objects.prefetch_related('section__course'), pk=content_id)
#     CompletedContent.objects.get_or_create(content=content, user=request.user)
    
#     next_content = Content.objects.filter(section=content.section, order__gt=content.order).order_by('order').first()


#     # Si existe un contenido siguiente al completado dentro de la misma seccion lo redireccionamos a ese
#     if next_content:
#         return redirect('student:course_lessons', slug=content.section.course.slug, content_id=next_content.pk)

#     # Si no hay un contenido seguiente en la misma seccion, vamos a buscar al seccion siguiente
#     next_section = Section.objects.filter(course=content.section.course, order__gt=content.section.order).order_by('order').first()

#     # Si no hay mas secciones, lo redirigimos a la seccion actual o current  que tiene seleccionada
#     if not next_section:
#         return redirect('student:course_lessons', slug=content.section.course.slug, content_id=content.pk)
    

#     # Si hubiera una seccion siguiente a la actual entonces buscamos el primer contenido de esta que seria el siguiente contenido
#     next_content = next_section.contents.order_by('order').first()



#     # Si esta seccion esta vacia, no tiene contenidos, no existe un next_content por ende lo rediccionamos a la misma url con el mismo contenido
#     if not next_content:
#         return redirect('student:course_lessons', slug=content.section.course.slug, content_id=content.pk)

#     # Caso que la siguiente seccion tuviese un contenido siguiente lo redireccionamos a ese como current content
#     return redirect('student:course_lessons', slug=content.section.course.slug, content_id=next_content.pk)






