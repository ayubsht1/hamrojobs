# Generated by Django 5.1.1 on 2024-11-17 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hamrojob', '0003_searchlog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='searchlog',
            old_name='query',
            new_name='search_query',
        ),
    ]
