# Generated by Django 3.1.1 on 2020-10-20 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0010_gradedassignment_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gradedassignment',
            name='progress',
            field=models.CharField(default='0%', max_length=4),
        ),
    ]
