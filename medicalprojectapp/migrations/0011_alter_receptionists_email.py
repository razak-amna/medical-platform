# Generated by Django 5.1.4 on 2025-01-12 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicalprojectapp', '0010_alter_receptionists_hire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receptionists',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
