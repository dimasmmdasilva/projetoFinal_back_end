# Generated by Django 5.1.1 on 2024-10-04 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_user_location"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="birth_date",
        ),
        migrations.RemoveField(
            model_name="user",
            name="location",
        ),
    ]