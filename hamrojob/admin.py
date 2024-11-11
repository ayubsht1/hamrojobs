from django.contrib import admin

# Register your models here.
from hamrojob.models import Job, JobCategory
from company.models import Company
admin.site.register([Job, JobCategory])
admin.site.register(Company)