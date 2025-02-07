# Generated by Django 5.1.2 on 2025-01-19 14:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_App', '0001_initial'),
        ('User_App', '0002_deliveryaddress_orders'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('CARD', 'Credit/Debit Card'), ('UPI', 'UPI'), ('PAYPAL', 'PayPal'), ('COD', 'Cash on Delivery'), ('BANK_TRANSFER', 'Bank Transfer')], max_length=15)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='Admin_App.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='User_App.viewers')),
            ],
        ),
    ]
