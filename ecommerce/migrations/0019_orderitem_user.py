# Generated by Django 3.2.9 on 2021-11-12 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '__first__'),
        ('ecommerce', '0018_alter_order_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.userprofile'),
        ),
    ]
