# Generated by Django 4.2.5 on 2023-09-25 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_employmentdetails_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employmentdetails',
            old_name='is_ten_ten',
            new_name='is_ten_ten_employee',
        ),
    ]
