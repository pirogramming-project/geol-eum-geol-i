# Generated by Django 5.1.5 on 2025-01-31 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_id',
            field=models.CharField(default='dbf8a4db', editable=False, max_length=100, unique=True),
        ),
    ]
