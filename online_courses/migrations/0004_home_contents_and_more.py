# Generated by Django 4.1.7 on 2023-03-31 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_courses', '0003_course_lesson'),
    ]

    operations = [
        migrations.CreateModel(
            name='Home_contents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='uploads/default-thumbnail.jpg', upload_to='uploads/%Y/%m/%d/')),
                ('discription', models.TextField(max_length=1000)),
                ('time', models.TimeField(auto_now=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='Course_curriculum',
            new_name='Course_curriculums',
        ),
        migrations.RenameModel(
            old_name='Course_lesson',
            new_name='Course_lessons',
        ),
        migrations.RenameField(
            model_name='course_lessons',
            old_name='curriculum',
            new_name='curriculums',
        ),
    ]
