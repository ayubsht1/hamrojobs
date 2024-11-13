from django.db import models
from company.models import Company
from users.models import User

# Create your models here.
class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    JOB_TYPES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('FreeLance', 'Freelance'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    ]

    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=12, choices=JOB_TYPES)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    experience = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} at {self.company}"
    
class ApplyJob(models.Model):
    status_choices = (
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
        ('Pending', 'Pending'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=status_choices, default='Pending')
