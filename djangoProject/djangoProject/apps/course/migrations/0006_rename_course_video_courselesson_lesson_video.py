# Generated by Django 3.2 on 2021-04-17 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_courselesson_course_video'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courselesson',
            old_name='course_video',
            new_name='Lesson_video',
        ),
    ]