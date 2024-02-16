from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import forms
from . import models
from random import choice
import string

# Create your views here.
def generate_id():
    characters = string.ascii_letters + string.digits
    id = ""
    return ''.join([choice(characters) for i in range(10)])
    for x in range(22):
        id+=choice(characters)
    return id

def generate_password():
    characters = string.ascii_letters + string.punctuation + string.digits
    password = ""
    for x in range(28):
        password+=choice(characters)
    return password

def index_view(request):
    courses = models.Courses.objects.all()
    return render(request, 'online_courses/index.html', {
        'courses':courses,
    })
def signup_view(request):
    signup_form = forms.signup_form()
    show_create = False

    if request.method == 'POST':
        #if 'password_button' in request.POST:
        #    if signup_form.is_valid:
        #        print('$$$$$$$$$$$$')
        #        password = request.POST.get('Password')
        #        try:
        #            User(username=request.session['email'],email=request.session['email'],password=password)
        #            request.session.clear()
        #            login(request, request.user)
        #            messages.success(request, 'Loged in successfully')
        #            return HttpResponseRedirect(reverse('account'))
        #        except KeyError:
        #            return HttpResponseRedirect(reverse('signup'))

        signup_form = forms.signup_form(request.POST)
        if  signup_form.is_valid:
            email = request.POST.get('email')
            request.session['email'] = email

            ##############################
            ####### User.objects.get_or_create()
            try:
                qs = User.objects.get(email = email)
                if qs:
                    messages.info(request, '''This email is in use to DS account!''')
                
            except User.DoesNotExist:
                show_create = True
                #system_pass=generate_password()
                ############################
                #####SEND AN EMAIL HERE#####
                messages.success(request, '''Create your password''')
                return render(request, 'online_courses/signup.html', {
                    'signup_form':signup_form,
                    'show_create':show_create,
                })
            except User.MultipleObjectsReturned:
                messages.warning(request, '''You already 
                    have an account related to this email!''')
            return HttpResponseRedirect(reverse('signup'))
        
        
    #if reques.GET:
    #passwd = request.GET.get('xfz233')
    #   
    #    if passwd == system_pass:
    #        user = User.objects.create(Username = email, email = email)
    #        user.save()
    #    else:
    #        messages.warning(request, '''Something went wrong,
    #          Please try again!''')
            
    return render(request, 'online_courses/signup.html', {
        'signup_form':signup_form,
        'show_create':show_create,
    })

def signin_vew(request):
    signin_form = forms.signin_form()
    if request.user.is_authenticated and not(request.user.is_anonymous):
        if request.user.is_staff:
            return HttpResponseRedirect(reverse('admin_account'))
        else:
            return HttpResponseRedirect(reverse('account'))
    if request.method == 'POST':
        signin_form = forms.signin_form(request.POST)
        if  signin_form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = authenticate(username = email, password = password)
                if user is not None:
                    login(request, user)
                    if request.user.is_staff:
                        messages.success(request, 'Loged in successfully')
                        return HttpResponseRedirect(reverse('admin_account'))
                    else:
                        messages.success(request, 'Loged in successfully')
                        return HttpResponseRedirect(reverse('account'))
                else:
                    messages.warning(request, 'Wrong username or password!')
                    return HttpResponseRedirect(reverse('signin'))
            except user.PermmisionDeniedError:
                pass
            
    return render(request, 'online_courses/signin.html', {
        'signin_form':signin_form,
    })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url=reverse_lazy('signin'))    
def account_view(request):
    username  =  request.user.get_username
    return render(request, 'online_courses/account_files/account.html', {
        'username':username,
    })

@login_required(login_url=reverse_lazy('signin')) 
def admin_account_view(request):
    fullname = request.user.get_username()
    return render(request, 'online_courses/admin_files/admin_account.html', {
        'fullname':fullname,
    })

@login_required(login_url=reverse_lazy('signin'))
def admin_courses(request):
    courses = models.Courses.objects.all()
    students_enrolled = User.objects.all()
    if 'delete_course' in request.POST:
        id = request.POST['deleted_coourse_id']
        try:
            course = models.Courses.objects.get(id = id)
            course.delete()
        except models.Courses.DoesNotExist:
            pass 
    #curriculums = models.Course_curriculums.objects.select_related().filter(courses = courses.id)
    #lessons = models.Course_lessons.objects.select_related().filter(courses = courses.id)
    return render(request, 'online_courses/admin_files/courses.html', {
        'courses':courses,
        'students_enrolled':students_enrolled,
    })

@login_required(login_url=reverse_lazy('signin'))
def admin_course_curriculum(request, id):
    course = models.Courses.objects.get(id = id)
    curriculums = models.Course_curriculums.objects.select_related().filter(courses = course.id)
    lessons = models.Course_lessons.objects.select_related().filter(courses = course.id)
    return render(request, 'online_courses/admin_files/course.html', {
        'course':course,
        'curriculums':curriculums,
        'lessons':lessons,
    })

@login_required(login_url=reverse_lazy('signin'))
def add_course(request):
    add_course_form = forms.addcourse_form()
    if request.method == "POST":
        if 'submmit_course' in request.POST:
            add_course_form = forms.addcourse_form(request)
            if add_course_form.is_valid:
                id = generate_id()
                title = request.POST['title']
                price = request.POST['price']
                description = request.POST['description']
                more = request.POST['more']
                if 'image' in request.FILES['image']:
                    image = request.FILES['image']
                course_created = models.Courses(
                    id=id,
                    title = title,
                    price = price,
                    description = description,
                    more = more,
                    image = image,
                    )
                
                course_created.save()
                course_created.user.add(request.user)
                course_created.save()
                return HttpResponseRedirect(f'/ad-created-course/{course_created.id}')

    
    return render(request, 'online_courses/admin_files/add_course.html', {
     'add_course_form':add_course_form,
     #'course_created':course_created,
    })

@login_required(login_url=reverse_lazy('signin'))
def created_course(request,id):
    course = models.Courses.objects.get(id = id)
    return render(request, 'online_courses/admin_files/created_course.html', {
      'course':course,  
    })

@login_required(login_url=reverse_lazy('signin'))
def create_curriculum(request, id):
        curriculum_form = forms.create_curriculum_form()
        course = models.Courses.objects.get(id = id)
        curriculums = models.Course_curriculums.objects.select_related().filter(courses = course.id)
        if request.method == "POST":
            if 'create_curriculum' in request.POST:
                curriculum_form = forms.create_lesson_form(request)
                if curriculum_form.is_valid:
                    name = request.POST['name']
                    created_curriculum = models.Course_curriculums(
                        name = name,
                        courses = course
                    )
                    created_curriculum.save()
                    return HttpResponseRedirect(f'/843s98eadmidfn235a/account/c/{course.id}')
              
            
        return render(request, 'online_courses/admin_files/create_curriculum.html', {
            'course':course,
            'curriculum_form':curriculum_form,
            'curriculums':curriculums,
    })

@login_required(login_url=reverse_lazy('signin'))
def create_lesson(request, id):
        lesson_form = forms.create_lesson_form()
        curriculum = models.Course_curriculums.objects.get(id = id)
        lessons = models.Course_lessons.objects.select_related().filter(courses = curriculum.courses.id)
        if request.method == "POST":
            if 'create_lesson' in request.POST:
                lesson_form = forms.create_lesson_form(request)
                if lesson_form.is_valid:
                    lesson_name = request.POST['lesson_name']
                    lesson_file = request.POST['lesson_file']
                    key_points = request.POST['key_points']
                    created_lesson = models.Course_lessons(
                        id = generate_id(),
                        lesson_name= lesson_name,
                        lesson_file = lesson_file,
                        key_points = key_points,
                        courses = curriculum.courses,
                        curriculums = curriculum
                    )
                    created_lesson.save()
                    return HttpResponseRedirect(f"/843s98eadmidfn235a/account/addcourse/lesson/{id}")
              
            
        return render(request, 'online_courses/admin_files/create_lesson.html', {
            'course':curriculum.courses,
            'lesson_form':lesson_form,
            'curriculum':curriculum,
            'lessons':lessons,
    })

@login_required(login_url=reverse_lazy('signin'))
def modify_course(request, id):
    course = models.Courses.objects.get(id = id)
    data = {'title':str(course.title),
            'price':course.price,
            'description':str(course.description),
            'more':str(course.more)
            }
    modify_form = forms.addcourse_form( initial = data)
    if request.POST:
        if modify_form.has_changed():
            fields = modify_form.changed_data
            if 'title' in fields:
                title = request.POST['title']
            else:
                title = course.title
            if 'price' in fields:
                price = request.POST['price']
            else:
                price = course.price
            if 'description' in fields:
                description = request.POST['description']
            else:
                description = course.description
            if 'more' in fields:
                more = request.POST['more']
            else:
                more = request.more
            
            course.title = title
            course.price = price
            course.description = description
            course.more = more
            course.save()
            course = models.Courses.objects.get(id = id)
            return  HttpResponseRedirect(f'/843s98eadmidfn235a/account/modify/{course.id}')



    return render(request, 'online_courses/admin_files/modify_course.html', {
        'modify_form':modify_form,
    })


@login_required(login_url=reverse_lazy('signin'))
def modify_lesson(request, id):
        lesson_form = forms.create_lesson_form()
        try:
            lesson = models.Course_lessons.objects.get(id = id)
            data = {
                'lesson_name':lesson.lesson_name,
                'lesson_file':lesson.lesson_file,
                'key_points':lesson.key_points,
            }
            lesson_form = forms.create_lesson_form(initial = data)
        except:
            models.Course_lessons
            pass
        if request.method == "POST":

            if 'modify_lesson' in request.POST:
                if lesson_form.is_valid:
                    if lesson_form.has_changed():
                        changed_data = lesson_form.changed_data
                        if 'lesson_name' in changed_data:
                            lesson.lesson_name = request.POST['lesson_name']
                        if 'lesson_file' in changed_data:
                            lesson.lesson_file = request.FILE['lesson_file']
                        if 'key_points' in changed_data:
                            lesson.key_points = request.POST['key_points']

                        lesson.save()
                        lesson = models.Course_lessons.objects.get(id = id)
                        return HttpResponseRedirect(f"/843s98eadmidfn235a/account/modifyl/{id}")
              
            
        return render(request, 'online_courses/admin_files/modify_lesson.html', {
            'course':lesson.courses,
            'lesson_form':lesson_form,
            'curriculum':lesson.curriculums,
            'lesson':lesson,
    })
#####################################################
################  END OF ADMIN VIEWS ################
@login_required(login_url=reverse_lazy('signin'))
def account_courses(request):
    try:
        courses = models.Courses.objects.filter(user = request.user)
    except models.Courses.DoesNotExist:
        courses = False
        pass
    
    return render(request, 'online_courses/account_files/courses.html', {
        'courses':courses,

    })

@login_required(login_url=reverse_lazy('signin'))
def account_course(request, id):
    course = models.Courses.objects.get(id = id)
    curriculums = models.Course_curriculums.objects.select_related().filter(courses = course.id)
    lessons = models.Course_lessons.objects.select_related().filter(courses = course.id)
    return render(request, 'online_courses/account_files/course.html', {
    'course':course,
    'curriculums':curriculums,
    'lessons':lessons,
    })

@login_required(login_url=reverse_lazy('signin'))
def account_lesson(request, id):
    lesson = models.Course_lessons.objects.get(id = id)

    return render(request, 'online_courses/account_files/course_lesson.html', {
    'lesson':lesson,
    })

def course_view(request, id):
    course = models.Courses.objects.get(id = id)
    curriculums = models.Course_curriculums.objects.select_related().filter(courses = course.id)
    lessons = models.Course_lessons.objects.select_related().filter(courses = course.id)
    authenticated = False
    enrolled = False

    if request.user.is_authenticated:
        authenticated = True
    try:
        user = course.user.get(username = request.user.get_username())
        if user:
            enrolled = True
    except User.DoesNotExist:
        pass
    

    if 'enroll-in-acourse' in request.POST:
        if authenticated:
            user = request.user
            course.user.add(user)
            course.save()
            messages.success(request, 'You have successfully Enrolled in this course')
            return HttpResponseRedirect(f'/course/{course.id}')
        elif request.user.is_anonymous:
            messages.info(request, 'You need to login into your account so as to be able to enroll in this course!')
            return HttpResponseRedirect(f'/course/{course.id}')
        else:
            messages.info(request, 'Something wen\'t wrong, Please try again later')
            return HttpResponseRedirect(f'/course/{course.id}')

    return render(request, 'online_courses/course.html', {
        'course':course,
        'curriculums':curriculums,
        'lessons':lessons,
        'enrolled': enrolled,
        'authenticated':authenticated,
    })

def course_lesson_view(request, id):
    lesson = models.Course_lessons.objects.get(id = id)
    authenticated = False
    enrolled = False
    try:
        user = lesson.courses.user.get(username = request.user.get_username())
        if user:
            enrolled = True
    except User.DoesNotExist:
        pass
    if request.user.is_authenticated:
        authenticated = True
    
    if 'enroll-in-acourse' in request.POST:
        if request.user.is_authenticated:
            user = request.user
            lesson.courses.user.add(user)
            lesson.save()
            messages.success(request, 'You have successfully Enrolled in this course')
            return HttpResponseRedirect(f'/a-course//{lesson.id}')
        elif request.user.is_anonymous:
            messages.info(request, 'You need to login into your account so as to be able to enroll in this course!')
            return HttpResponseRedirect(f'/course/course-lesson/{lesson.id}')
        else:
            messages.info(request, 'Something wen\'t wrong, Please try again later')
            return HttpResponseRedirect(f'/course/course-lesson{lesson.id}')
    return render(request, 'online_courses/course_lesson.html', {
    'lesson':lesson,
    'authenticated': authenticated,
    'enrolled':enrolled,
    })

    


def flight(request):
    a_flight = models.Flight.passengers.all()
    lag=models.Passengers.objects.all().values('name')
    return render(request, "online_courses/testing.html", {
        'a_flight':a_flight,
        'lag':lag
    })
