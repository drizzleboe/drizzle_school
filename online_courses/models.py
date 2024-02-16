from django.db import models
from django.contrib.auth.models import User
from random import choice
import string



# Create your models here.

class Courses(models.Model):
    id = models.CharField(primary_key=True,unique=True, max_length=22)
    title   = models.CharField(max_length=80, null=True)
    price = models.IntegerField(null=True, blank=True)
    description =models.TextField(max_length=500, null=True, blank=True)
    more = models.TextField(max_length=20000, null=True, blank=True)
    time  = models.TimeField(auto_now=True)
    date  = models.DateField(auto_now=True)
    image  = models.ImageField(upload_to='uploads/%Y/%m/%d/', default="uploads/image-icon.jpg")
    def __str__(self):
        return f'{self.title} - {self.date}'
    user = models.ManyToManyField(User, related_name="students")

class Course_curriculums(models.Model):
    name = models.CharField(max_length=30, blank=False)   
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name="days")
    def __str__(self) -> str:
        return self.name

class Course_lessons(models.Model):
    id = models.CharField(primary_key=True,unique=True, max_length=22)
    lesson_name =  models.CharField(max_length=70, blank=False, null=False)
    lesson_file= models.FileField(upload_to='uploads/tutorials/videos/', null=True)
    key_points = models.TextField(max_length=1000, blank=False, null=False)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name="thetop")
    curriculums = models.ForeignKey(Course_curriculums, on_delete=models.CASCADE)
    visited = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.lesson_name
    
class Home_contents(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, default="uploads/default-thumbnail.jpg")
    discription = models.TextField(max_length=1000)
    time        = models.TimeField(auto_now=True)

    def __str__(self) -> str:
        return self.discription

class Flight(models.Model):
    f_from = models.CharField(max_length=24)
    f_to = models.CharField(max_length=45)
    duration =models.IntegerField()

class Passengers(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='passengers')
    name = models.CharField(max_length=24)

class laguage(models.Model):
    owner = models.ForeignKey(Passengers, on_delete=models.CASCADE, related_name="pass_lag")
    kg = models.IntegerField()
