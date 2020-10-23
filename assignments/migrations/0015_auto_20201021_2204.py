# Generated by Django 3.1.1 on 2020-10-21 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0014_studentanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentanswer',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentanswer',
            name='progress',
            field=models.CharField(default='0%', max_length=4),
        ),
    ]
