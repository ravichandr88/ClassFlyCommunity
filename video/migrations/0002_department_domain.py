# Generated by Django 2.2.4 on 2020-11-23 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='domain',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='video.EducationDomain'),
        ),
    ]
