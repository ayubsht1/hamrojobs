from django.db import models

# Create your models here.
class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class JobLocation(models.Model):
    city =models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country =models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city}, {self.state}, {self.country}"


class Job(models.Model):
    JOB_TYPES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('FreeLance', 'Freelance'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    ]

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(JobLocation, on_delete=models.SET_NULL, null=True)
    job_type = models.CharField(max_length=12, choices=JOB_TYPES)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField()
    experience = models.PositiveIntegerField()
    contact_email = models.EmailField()

    def __str__(self):
        return f"{self.title} at {self.company}"
