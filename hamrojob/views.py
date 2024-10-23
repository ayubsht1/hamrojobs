from typing import Any
from django.shortcuts import render
from django.views.generic import (
    TemplateView, ListView, DetailView
)
from hamrojob.models import (
    Job, JobCategory, JobLocation
)
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

class JobView(ListView):
    model = Job
    template_name = 'job/job_list.html'
    context_object_name = "jobs"
    paginate_by = 3  # Number of jobs per page

    def get_queryset(self):
        # Ordering jobs by the 'posted_at' field in descending order
        return Job.objects.order_by("-posted_at")

    def get_context_data(self, **kwargs):
        # Let ListView handle the pagination
        context = super().get_context_data(**kwargs)
        return context

class JobDetailView(TemplateView):
    template_name = 'job/job_detail.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

class AboutView(TemplateView):
    template_name = 'about.html'