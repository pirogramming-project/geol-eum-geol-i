# Generated by Django 5.1.5 on 2025-01-31 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_id',
            field=models.CharField(default='abda38bf', editable=False, max_length=100, unique=True),
        ),
    ]
