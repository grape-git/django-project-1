# Generated by Django 3.2.3 on 2021-06-03 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogsapp', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
