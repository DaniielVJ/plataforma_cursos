# shortchut que ahorra el hacer un 404 si el objeto a buscar no existe
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Course

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

    return render(request, 'courses/course_detail.html', {'course': course})


def course_lessons(request, slug):
    course = get_object_or_404(Course, slug=slug)
    course_title = course.title
    sections = course.sections.prefetch_related('contents')
    
    return render(request, 'courses/course_lessons.html', {'course_title': course_title, 'sections': sections })

