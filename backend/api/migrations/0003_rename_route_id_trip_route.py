# Generated by Django 4.1.4 on 2022-12-16 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_route_route_desc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='route_id',
            new_name='route',
        ),
    ]
