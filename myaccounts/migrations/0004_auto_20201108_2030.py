# Generated by Django 3.1.3 on 2020-11-08 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myaccounts', '0003_auto_20201108_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='department',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]