# Generated by Django 4.2.5 on 2023-10-01 01:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lists", "0003_list_item_list"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="priority",
            field=models.TextField(default=""),
        ),
    ]
