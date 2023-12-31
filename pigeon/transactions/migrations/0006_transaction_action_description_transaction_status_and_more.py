# Generated by Django 4.2.7 on 2023-12-11 12:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_buyer_seller'),
        ('transactions', '0005_alter_transaction_buyer_alter_transaction_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='action_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('IP', 'In Progress'), ('C', 'Completed'), ('X', 'Canceled'), ('AR', 'Action Required')], default='P', max_length=2),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buyer_transactions', to='accounts.buyer'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seller_transactions', to='accounts.seller'),
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_timestamp', models.DateTimeField(auto_now_add=True)),
                ('action_description', models.TextField()),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.transaction')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
