# Generated by Django 4.2.5 on 2023-09-25 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_alter_coach_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmploymentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ten_ten', models.BooleanField()),
                ('is_vtc_coach', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='TenTenEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wage', models.FloatField()),
                ('is_contract', models.BooleanField()),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ten_ten_details', to='registration.employmentdetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VTCEmployee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wage', models.FloatField()),
                ('is_contract', models.BooleanField()),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vtc_details', to='registration.employmentdetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Coach',
        ),
    ]
