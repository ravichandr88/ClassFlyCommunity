# Generated by Django 2.2.4 on 2021-06-18 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('interview', '0003_professional_meeting'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('address', models.TextField(max_length=500)),
                ('city', models.CharField(max_length=50)),
                ('company_linkedin_url', models.URLField()),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HRaccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=50, null=True)),
                ('linkedin_url', models.URLField()),
                ('office_email', models.EmailField(max_length=254)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='hraccount', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
