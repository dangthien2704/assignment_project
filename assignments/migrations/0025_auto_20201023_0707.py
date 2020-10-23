# Generated by Django 3.1.1 on 2020-10-23 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignments', '0024_auto_20201022_2254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gradedassignment',
            name='answer_text',
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.CharField(default='0%', max_length=4)),
                ('completed', models.BooleanField(default=False)),
                ('grade', models.IntegerField(default=0)),
                ('answer_text', models.CharField(blank=True, max_length=100)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignments.assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_answer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]