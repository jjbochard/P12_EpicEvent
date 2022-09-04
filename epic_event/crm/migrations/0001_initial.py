# Generated by Django 4.0 on 2022-09-04 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('fix_phone', models.CharField(max_length=12, unique=True)),
                ('mobile_phone', models.CharField(max_length=12, unique=True)),
                ('status', models.CharField(choices=[('POTENTIAL', 'Potential'), ('ACTUAL', 'Actual')], default='POTENTIAL', max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_signed', models.BooleanField(default=False)),
                ('amount', models.FloatField()),
                ('payment_due', models.DateTimeField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendees', models.IntegerField(default=0)),
                ('notes', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('is_finished', models.BooleanField(default=False)),
            ],
        ),
    ]
