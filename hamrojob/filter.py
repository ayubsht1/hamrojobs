import django_filters
from . models import Job,JobCategory
from django import forms

class Jobfilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = ['title', 'job_type', 'job_type', 'is_available' ]

class Jobfilter(django_filters.FilterSet):
    # Job category as checkboxes
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=JobCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Job Category"
    )
    
    # Job type as checkboxes
    job_type = django_filters.MultipleChoiceFilter(
        choices=[
            ('Full Time', 'Full Time'),
            ('Part Time', 'Part Time'),
            ('Remote', 'Remote'),
            ('Freelance', 'Freelance')
        ],
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Job
        fields = ['category', 'job_type']