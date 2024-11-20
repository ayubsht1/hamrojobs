from django.contrib import admin
from users.models import User
# Register your models here.
from hamrojob.models import JobCategory

admin.site.register( JobCategory)
admin.site.register(User)