# Generated by Django 4.0 on 2022-09-13 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0006_rename_error_field_log_field_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="date",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]