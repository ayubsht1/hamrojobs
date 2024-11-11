from django.db import models
from users.models import User

class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    job_title = models.CharField(max_length=100)

    #insert cv
    def __str__(self):
        return f'{self.first_name} {self.surname}'