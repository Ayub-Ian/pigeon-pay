# Generated by Django 4.2.7 on 2023-12-19 13:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_transaction_action_description_transaction_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='fee_paid_by',
            field=models.CharField(choices=[('buyer', 'Buyer'), ('seller', 'Seller'), ('split', 'Split')], default='split', max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
