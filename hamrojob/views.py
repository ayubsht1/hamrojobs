from django.views.generic import ListView, TemplateView, DetailView, View
from hamrojob.models import Job, JobCategory, ApplyJob
from django.shortcuts import render, redirect
from django.contrib import messages
from .form import CreateJobForm, UpdateJobForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .filter import Jobfilter
from django_filters.views import FilterView
from django.db.models import Q, Count


# Home view to show a list of jobs
class HomeView(FilterView):
    model = Job
    template_name = 'home.html'
    context_object_name = "jobs"
    filterset_class = Jobfilter
    paginate_by = 3

    def get_queryset(self):
        return Job.objects.filter(is_available=True).order_by("-posted_at")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()  # Add categories from another model
        filterset = self.filterset_class(self.request.GET, queryset=Job.objects.filter(is_available=True))
        context['filter'] = filterset
        return context

# Job view to list all jobs
class JobView(FilterView):
    model = Job
    template_name = 'job/job_list.html'
    context_object_name = "jobs"
    paginate_by = 3
    filterset_class = Jobfilter

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_available=True).order_by("-posted_at")
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_jobs = self.get_queryset().count()        
        context['company_logos'] = {job.id: job.company.logo.url if job.company.logo else None for job in context['jobs']}
        context['total_job_count'] = total_jobs
        context['filter'] = self.filterset
        return context

# Category view to list all job categories
class CategoryView(ListView):
    model = JobCategory
    template_name = 'job/job_list_left.html'
    context_object_name = "categories"

    def get_queryset(self):
        return JobCategory.objects.all()

# Job detail view for displaying job details
class JobDetailView(LoginRequiredMixin, DetailView):
    model = Job
    context_object_name = 'job'

    def get_template_names(self):
        if self.request.user.is_recruiter:
            return ['job/edit_details.html']
        else:
            return ['job/job_detail.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     
        company = context['job'].company
        context['company_logo'] = company.logo 
        user = self.request.user
        job = self.get_object()  
        context['has_applied'] = ApplyJob.objects.filter(user=user, job=job).exists()

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
    
def manage_jobs(request):
    jobs = Job.objects.filter(user=request.user, company=request.user.company).order_by("-posted_at")
    total_jobs = jobs.count()
    paginator = Paginator(jobs, 3)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'jobs': page_obj.object_list,  
        'page_obj': page_obj,  
        'total_job_count': total_jobs,  
    }
    return render(request, 'job/manage_jobs.html', context)

def apply_to_job(request, pk):
    if request.user.is_authenticated:
        if request.user.is_applicant:
            job = Job.objects.get(pk=pk)
            if ApplyJob.objects.filter(user=request.user, job=pk).exists():
                messages.warning(request, 'Permission Denied')
                return redirect('home')
            else:
                ApplyJob.objects.create(
                    job=job,
                    user = request.user,
                    status = 'Pending'
                )
                messages.info(request, 'You have successfully applied ! Please see dashboard')
                return redirect('home')
        else:
            messages.info(request, 'Invalid Request you are not an applicant            q')
            return redirect('home')
    else:
        return redirect('login')
    
def all_applicants(request, pk):
    job = Job.objects.get(pk=pk)
    applicants= job.applyjob_set.all()
    context = {'job':job, 'applicants':applicants}
    return render(request, 'job/all_applicants.html', context)

def applied_jobs(request):
    jobs= ApplyJob.objects.filter(user=request.user)
    context = {'jobs':jobs}
    return render(request, 'job/applied_job.html', context)


class JobSearchView(View):
    def get(self, request, *args, **kwargs):
        # Choose template based on user type
        if request.user.is_authenticated and request.user.is_recruiter:
            template_name = "job/manage_jobs.html"
        else:
            template_name = "job/job_list.html"
        
        query = request.GET.get('query', '')

        # Filter jobs by availability
        job_list = Job.objects.filter(is_available=True)

        # Apply search filters
        if query:
            job_list = job_list.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query) |
                Q(company__name__icontains=query) |
                Q(job_type__icontains=query) |
                Q(experience__icontains=query)
            )

        # Get the total job count before pagination
        total_jobs = job_list.count()

        # Order jobs and apply pagination
        job_list = job_list.order_by("-posted_at")
        page = request.GET.get("page", 1)
        paginator = Paginator(job_list, 5)
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)

        # Render the template with additional context
        return render(
            request, 
            template_name, 
            {
                "title": "Job Search",
                "page_obj": jobs,  # for pagination controls
                "jobs": jobs,
                "query": query,
                "total_job_count": total_jobs,  # Total job count without pagination
            }
        )
    
class JobListByCategoryView(ListView):
    model = Job
    template_name = "job/job_list.html"
    context_object_name = "jobs"
    paginate_by = 3

    def get_queryset(self):
        # Filter jobs by availability and selected category ID
        return Job.objects.filter(
            is_available=True,
            category__id=self.kwargs["category_id"]
        ).order_by("-posted_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve all categories and manually count available jobs for each
        categories = JobCategory.objects.all()
        for category in categories:
            category.job_count = Job.objects.filter(
                category=category,
                is_available=True
            ).count()

        # Add context variables for the template
        context['title'] = 'Jobs by Category'
        context['categories'] = categories
        context['selected_category_id'] = self.kwargs["category_id"]

        # Add total job count for the selected category only
        selected_category = JobCategory.objects.get(id=self.kwargs["category_id"])
        context['total_job_count'] = Job.objects.filter(
            is_available=True,
            category=selected_category
        ).count()

        # Pagination logic (manually handle pagination)
        jobs = self.get_queryset()
        paginator = Paginator(jobs, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context