from django.shortcuts import render

# Create your views here.


def courses_list(request):
    return render(request, 'courses/courses.html')


def course_detail(request):
    pass



def course_lessons(request):
    pass