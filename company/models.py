from django.db import models
from users.models import User

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100 , null=True, blank=True)
    est_date = models.PositiveIntegerField(null=True, blank=True)
    city = models.CharField(max_length=100 , null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to='company_images/', null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name