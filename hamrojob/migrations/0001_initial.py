# Generated by Django 5.1.1 on 2024-10-21 06:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='JobLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
                ('job_type', models.CharField(choices=[('FT', 'Full Time'), ('PT', 'Part Time'), ('FL', 'Freelance'), ('IN', 'Internship'), ('RM', 'Remote')], max_length=2)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('salary_min', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('salary_max', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('application_deadline', models.DateTimeField()),
                ('experience', models.PositiveIntegerField()),
                ('contact_email', models.EmailField(max_length=254)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hamrojob.jobcategory')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hamrojob.joblocation')),
            ],
        ),
    ]