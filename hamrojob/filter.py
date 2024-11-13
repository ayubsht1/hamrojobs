import django_filters
from . models import Job

class Jobfilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = ['title', 'job_type', 'job_type', 'is_available' ]