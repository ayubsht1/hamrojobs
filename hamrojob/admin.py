from django.contrib import admin
from users.models import User
# Register your models here.
from hamrojob.models import Job, JobCategory
from company.models import Company
admin.site.register([Job, JobCategory])
admin.site.register(Company)
admin.site.register(User)