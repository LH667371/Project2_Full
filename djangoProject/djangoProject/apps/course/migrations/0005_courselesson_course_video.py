# Generated by Django 3.2 on 2021-04-17 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_course_course_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='courselesson',
            name='course_video',
            field=models.FileField(blank=True, null=True, upload_to='video', verbose_name='视频'),
        ),
    ]