from django.contrib import admin
from . import models
# Register your models here.
class course_view(admin.ModelAdmin):
    list_display=['title', 'price','description']
    list_filter = ['date','price']


class Course_curriculums_view(admin.ModelAdmin):
    list_display= ['name']

class Course_lessons_view(admin.ModelAdmin):
    list_display = ['lesson_name','courses','curriculums']
admin.site.register(models.Courses, course_view)
admin.site.register(models.Course_curriculums, Course_curriculums_view)
admin.site.register(models.Course_lessons,Course_lessons_view)
admin.site.register(models.Flight)
admin.site.register(models.Passengers)
admin.site.register(models.laguage)