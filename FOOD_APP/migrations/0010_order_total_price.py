# Generated by Django 5.0.1 on 2024-02-07 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FOOD_APP', '0009_order_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]