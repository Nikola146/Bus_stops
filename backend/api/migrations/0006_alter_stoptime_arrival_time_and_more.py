# Generated by Django 4.1.4 on 2022-12-16 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_time_stoptime_alter_stoptime_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stoptime',
            name='arrival_time',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='stoptime',
            name='departure_time',
            field=models.CharField(max_length=8),
        ),
    ]
