# Generated by Django 4.2.1 on 2023-06-02 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planrow',
            name='name',
        ),
    ]
