# Generated by Django 4.0 on 2022-08-22 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0003_remove_client_company"),
    ]

    operations = [
        migrations.AlterField(
            model_name="department",
            name="department",
            field=models.CharField(max_length=105),
        ),
    ]
