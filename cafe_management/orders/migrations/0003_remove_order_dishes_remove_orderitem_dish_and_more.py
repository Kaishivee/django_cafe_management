# Generated by Django 5.1.7 on 2025-03-06 23:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_dish_remove_order_items_alter_order_status_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="dishes",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="dish",
        ),
        migrations.RemoveField(
            model_name="orderitem",
            name="order",
        ),
        migrations.AddField(
            model_name="order",
            name="items",
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name="order",
            name="table_number",
            field=models.IntegerField(
                validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
        migrations.DeleteModel(
            name="Dish",
        ),
        migrations.DeleteModel(
            name="OrderItem",
        ),
    ]
