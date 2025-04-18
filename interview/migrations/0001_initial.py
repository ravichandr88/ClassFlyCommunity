# Generated by Django 2.2.4 on 2021-06-07 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fresher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college', models.CharField(max_length=40)),
                ('branch', models.CharField(max_length=50)),
                ('passout_year', models.IntegerField()),
                ('about_yourself', models.CharField(max_length=500, null=True)),
                ('total_experience', models.FloatField()),
                ('resume_url', models.URLField(null=True)),
                ('skills', models.CharField(default='', max_length=500)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='applicant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exp_company', models.CharField(max_length=80)),
                ('exp_work', models.CharField(max_length=500)),
                ('exp_period', models.CharField(max_length=40)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experience', to='interview.Fresher')),
            ],
        ),
    ]
