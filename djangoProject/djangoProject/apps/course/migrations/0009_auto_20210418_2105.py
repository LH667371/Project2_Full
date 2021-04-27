# Generated by Django 3.2 on 2021-04-18 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0008_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='create_time',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='is_show',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='orders',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='update_time',
        ),
        migrations.AlterField(
            model_name='comment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_comment', to='course.course', verbose_name='评论课程'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_id', to=settings.AUTH_USER_MODEL, verbose_name='评论用户'),
        ),
    ]
