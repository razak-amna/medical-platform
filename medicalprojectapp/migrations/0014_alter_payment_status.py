# Generated by Django 5.1.4 on 2025-01-16 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicalprojectapp', '0013_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(default='Success', max_length=50),
        ),
    ]
