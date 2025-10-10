from django.shortcuts import render

# Create your views here.

# Datos ficticios para simular una base de datos

courses= [ # doomy data
    {
        "id": 1, "name": "python", "level": "beginner", "rating": 5.0, 
        "title": "Three-month Course to Learn the Basics of Python and StartCoding.",
        "author": "Alison Walsh JIIJIIJIJIJIJIJIJI", "course_img": "images/curso_1.jpg", 
        "author_img": 'https://randomuser.me/api/portraits/women/68.jpg',
     },
    {
        "id": 2, "name": "django", "level": "beginner", "rating": 4.1, 
        "title": "Beginner's Guide to Successful Company Management: Business And More",
        "author": "Patty Kutch", "course_img": "images/curso_2.jpg", 
        "author_img": 'https://randomuser.me/api/portraits/women/20.jpg',
    },
    {
        "id": 2, "name": "django_avanzado" , "level": "advanced", "rating": 4.7, 
        "title": "A Fascinating Theory of Probability. Practice. Application. How to Outplay...",
        "author": "Alonzo Murray", "course_img": "images/curso_3.jpg", 
        "author_img": 'https://randomuser.me/api/portraits/men/32.jpg', 
    },
    {
        "id": 2, "name": "fastapi_avanzado" , "level": "advanced", "rating": 4.9, 
        "title": "Introduction: Machine Learning and LLM. Implementation in Modern Software",
        "author": "Gregory Harris", "course_img": "images/curso_4.jpg", 
        "author_img": 'https://randomuser.me/api/portraits/men/45.jpg',
    }
    
]


def courses_list(request):
    # Version para probar antes de irme
    # return render(request, 'courses/courses.html', {'course': courses[0]})


    # Original a usar luego
    return render(request, 'courses/courses.html', {'courses': courses})


def course_detail(request, name:str = ""):
    # Pasamos un curso ficticio que definimos en duro su informacion, pero en un entorno
    # real se van a buscar los datos del curso solicitado a la base de datos y los datos o campos
    # obtenidos se pasan al template encargado de mostrar los detalles de un curso cuando se selecciona
    
    # Aqui definimos mas campos que podria tener el curso, donde le damos una estructura a esos datos
    # con diccionario, representanto una estructura de documentos como en mongodb
    course={
        'course_title': "Django Aplicaciones Web Robustas",
        'course_link': 'course_lessons',
        'course_img': 'images/curso_2.jpg',
        'course_info': {
            'lessons': 100,
            'duration': 54,
            'instructor': 'Daniel Valdebenito',
            'instructor_img': 'https://randomuser.me/api/portraits/men/15.jpg',
            },
        'course_content': [
            {
                'id': 1,
                'name': 'Introduccion al curso',
                'lessons': [
                    {
                        'name': '¿Que aprenderas en este curso?',
                        'type': 'video' 
                    },
                    {
                        'name': 'Como usar la plataforma',
                        'type': 'article'
                    }
                ]
            },
            {
                'id': 2,
                'name': 'Introduccion al curso',
                'lessons': [
                    {
                        'name': '¿Que aprenderas en este curso?',
                        'type': 'video' 
                    },
                    {
                        'name': 'Como usar la plataforma',
                        'type': 'article'
                    }
                ]
            }
        ]
    }
    
    
    return render(request, 'courses/course_detail.html', {'course': course})



def course_lessons(request):
    return render(request, 'courses/course_lessons.html')