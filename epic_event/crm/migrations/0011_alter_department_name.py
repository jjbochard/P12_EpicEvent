# Generated by Django 4.0 on 2022-08-27 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0010_alter_client_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="department",
            name="name",
            field=models.CharField(max_length=255),
        ),
    ]
