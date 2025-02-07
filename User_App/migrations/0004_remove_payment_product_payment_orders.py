# Generated by Django 5.1.2 on 2025-01-20 06:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_App', '0003_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='product',
        ),
        migrations.AddField(
            model_name='payment',
            name='orders',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='User_App.buynow'),
        ),
    ]
