from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

class JobView(TemplateView):
    template_name = 'job/job_list.html'

class JobDetailView(TemplateView):
    template_name = 'job/job_detail.html'

class ContactView(TemplateView):
    template_name = 'contact.html'