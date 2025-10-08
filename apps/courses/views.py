from django.shortcuts import render

# Create your views here.

# Datos ficticios para simular una base de datos

doomy_data = [
    {
        "id": 1, "name": "django", "level": "beginner", "rating": 5.0, 
        "title": "Three-month Course to Learn the Basics of Python and StartCoding.",
        "author": "Alison Walsh JIIJIIJIJIJIJIJIJI",
     },
    {
        
    }
    
]


def courses_list(request):
    # Version para probar antes de irme
    return render(request, 'courses/courses.html', {'course': doomy_data[0]})


    # Original a usar luego
    return render(request, 'courses/courses.html', {'list_courses': doomy_data})


def course_detail(request, name:str = ""):
    return render(request, 'courses/course_detail.html')



def course_lessons(request):
    pass