# Generated by Django 2.2.8 on 2021-07-16 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0013_delete_professionaltimetable'),
    ]

    operations = [
        migrations.AddField(
            model_name='fresher',
            name='profile_pic',
            field=models.URLField(default='https://ggg'),
        ),
    ]
