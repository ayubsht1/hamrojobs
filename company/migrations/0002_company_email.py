# Generated by Django 5.1.1 on 2024-11-11 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
