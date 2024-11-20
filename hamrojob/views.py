from django.views.generic import ListView, TemplateView, DetailView, View
from hamrojob.models import Job, JobCategory, ApplyJob
from django.shortcuts import render, redirect
from django.contrib import messages
from .form import CreateJobForm, UpdateJobForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .filter import Jobfilter
from django_filters.views import FilterView
from django.db.models import Q
from .models import SearchLog


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
        context['categories'] = JobCategory.objects.all() 
        filterset = self.filterset_class(self.request.GET, queryset=Job.objects.filter(is_available=True))
        context['filter'] = filterset
        return context

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
        filtered_queryset = self.get_queryset()
        filters_applied = any(value for key, value in self.request.GET.items() if key in self.filterset_class.get_fields())
        context['company_logos'] = {
            job.id: job.company.logo.url if job.company.logo else None for job in context['jobs']
        }
        if not filters_applied:
            context['total_job_count'] = filtered_queryset.count()
        
        context['filter'] = self.filterset  
        return context


class CategoryView(ListView):
    model = JobCategory
    template_name = 'job/job_list_left.html'
    context_object_name = "categories"

    def get_queryset(self):
        return JobCategory.objects.all()


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
        if request.user.is_applicant and request.user.has_resume:
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
            messages.info(request, 'Invalid Request, you do not have permission')
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
        if request.user.is_authenticated and request.user.is_recruiter:
            template_name = "job/manage_jobs.html"
        else:
            template_name = "job/job_list.html"
        
        query = request.GET.get('query', '')

        if query and request.user.is_authenticated:
            if hasattr(request.user, 'is_applicant') and request.user.is_applicant:
                SearchLog.objects.create(user=request.user, search_query=query)

        job_list = Job.objects.filter(is_available=True)

        if query:
            job_list = job_list.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query) |
                Q(company__name__icontains=query) |
                Q(job_type__icontains=query) |
                Q(experience__icontains=query)
            )

        total_jobs = job_list.count()

        job_list = job_list.order_by("-posted_at")
        paginator = Paginator(job_list, 5)  
        page = request.GET.get("page", 1)

        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)

        is_paginated = jobs.has_other_pages()
        return render(
            request, 
            template_name, 
            {
                "title": "Job Search",
                "page_obj": jobs,  
                "jobs": jobs,      
                "query": query,    
                "total_job_count": total_jobs,  
                "is_paginated": is_paginated,   
            }
        )
    
class JobListByCategoryView(ListView):
    model = Job
    template_name = "job/job_list.html"
    context_object_name = "jobs"
    paginate_by = 3

    def get_queryset(self):
        return Job.objects.filter(
            is_available=True,
            category__id=self.kwargs["category_id"]
        ).order_by("-posted_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
    
class JobRecommendationsView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'job/job_recommendations.html'
    context_object_name = 'recommended_jobs'
    paginate_by = 5  # Use Django's built-in pagination

    def get_queryset(self):
        """Generate job recommendations based on the user's recent search logs."""
        if self.request.user.is_applicant:
            # Fetch the 5 most recent search logs for the user
            search_logs = SearchLog.objects.filter(user=self.request.user).order_by('-created_at')[:5]
            if not search_logs.exists():
                return Job.objects.none()

            # Build a query for recommendations based on search terms
            search_terms = [log.search_query for log in search_logs]
            query = Q()
            for term in search_terms:
                query |= (
                    Q(title__icontains=term) |
                    Q(location__icontains=term) |
                    Q(company__name__icontains=term)
                )

            # Filter jobs based on search terms
            return Job.objects.filter(query, is_available=True).distinct().order_by('-posted_at')
        else:
            return Job.objects.none()

    def get_context_data(self, **kwargs):
        """Add pagination and other context data to the template."""
        context = super().get_context_data(**kwargs)

        # Add custom pagination logic for consistency with get_queryset()
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page = self.request.GET.get('page', 1)
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)

        context.update({
            'recommended_jobs': jobs,
            'is_paginated': jobs.has_other_pages(),
            'title': 'Recommended Jobs',
        })

        return context