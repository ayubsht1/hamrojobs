# Generated by Django 5.1.1 on 2024-11-13 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0003_resume_upload_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='upload_resume',
            field=models.FileField(blank=True, null=True, upload_to='resume'),
        ),
    ]
