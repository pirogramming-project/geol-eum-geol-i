# Generated by Django 5.1.5 on 2025-01-30 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='start_location',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
