from django.contrib import admin

# Register your models here.
from hamrojob.models import Job, JobCategory, JobLocation
admin.site.register([Job, JobCategory, JobLocation])