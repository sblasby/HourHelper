# Generated by Django 4.2.5 on 2023-09-26 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_employmentdetails_first_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employmentdetails',
            name='first_login',
            field=models.BooleanField(default=True),
        ),
    ]
