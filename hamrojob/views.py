from django.views.generic import ListView, TemplateView, DetailView
from hamrojob.models import Job, JobCategory
from django.shortcuts import render, redirect
from django.contrib import messages
from .form import CreateJobForm, UpdateJobForm

# Home view to show a list of jobs
class HomeView(ListView):
    model = Job
    template_name = 'home.html'
    context_object_name = "jobs"
    paginate_by = 3

    def get_queryset(self):
        return Job.objects.order_by("-posted_at")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()  # Add categories from another model
        return context

# Job view to list all jobs
class JobView(ListView):
    model = Job
    template_name = 'job/job_list.html'
    context_object_name = "jobs"
    paginate_by = 3

    def get_queryset(self):
        return Job.objects.order_by("-posted_at")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add company logos to the context for each job
        context['company_logos'] = {job.id: job.company.logo.url if job.company.logo else None for job in context['jobs']}
        return context

# Category view to list all job categories
class CategoryView(ListView):
    model = JobCategory
    template_name = 'job/job_list_left.html'
    context_object_name = "categories"

    def get_queryset(self):
        return JobCategory.objects.all()

# Job detail view for displaying job details
class JobDetailView(DetailView):
    model = Job
    template_name = 'job/job_detail.html'
    context_object_name = 'job'  # The object in the context will be named 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch the related company details
        company = context['job'].company
        context['company_logo'] = company.logo  # Pass the company logo to the template
        return context

class ContactView(TemplateView):
    template_name = 'contact.html'

class AboutView(TemplateView):
    template_name = 'about.html'


def create_job(request):
    if request.user.is_authenticated:
        if request.user.is_recruiter and request.user.has_company:
            if request.method == 'POST':
                form = CreateJobForm(request.POST)
                if form.is_valid():
                    var = form.save(commit=False)
                    var.user = request.user
                    var.company = request.user.company
                    var.save()
                    messages.warning(request, 'new job has been created')
                    return redirect('dashboard')
                else:
                    messages.warning(request, 'something went wrong')
                    return redirect('create-job')
            else:
                form = CreateJobForm()
                context = {'form':form}
                return render(request, 'job/create_job.html',context) 
        else:
            messages.warning(request,'Permission Denied')
            return redirect('home')
    else:
        messages.warning(request,'Permission Denied')
        return redirect('home')
    
def update_job(request, pk):
    if request.user.is_authenticated:
        if request.user.is_recruiter and request.user.has_company:
            job = Job.objects.get(pk=pk)
            if request.method == 'POST':
                form = UpdateJobForm(request.POST, instance=job)
                if form.is_valid():
                    form.save()
                    messages.info(request, 'Your job info is updated')
                    return redirect('dashboard')
                else:
                    messages.warning(request, 'something went wrong')
            else:
                form = UpdateJobForm(instance=job)
                context = {'form':form}
                return render(request, 'job/update_job.html',context) 
        else:
            messages.warning(request,'Permission Denied')
            return redirect('home')
    else:
        messages.warning(request,'Permission Denied')
        return redirect('home')