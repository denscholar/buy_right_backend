# Generated by Django 5.1.3 on 2024-11-19 02:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_alter_category_options_alter_category_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=150, unique=True),
        ),
    ]