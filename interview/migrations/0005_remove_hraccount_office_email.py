# Generated by Django 2.2.4 on 2021-06-18 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0004_company_hraccount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hraccount',
            name='office_email',
        ),
    ]
