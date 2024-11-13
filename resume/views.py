from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Resume
from users.models import User
from .form import UpdateResumeForm

def update_resume(request):
    if request.user.is_applicant:
        resume = Resume.objects.get(user=request.user)
        if request.method == 'POST':
            form = UpdateResumeForm(request.POST, request.FILES, instance=resume)
            if form.is_valid():
                var = form.save(commit=False)
                user = User.objects.get(pk=request.user.id)
                user.has_resume = True
                user.save()
                var.save()
                messages.info(request, 'Your Resume info has been updated.')
                return redirect('dashboard')
            else:
                messages.warning('something went wrong')
        else:
            form = UpdateResumeForm(instance=resume)
            context = {'form':form}
            return render(request, 'resume/update_resume.html', context)
    else:
        messages.warning(request,"Permission denied")
        return redirect('dashboard')
        

def resume_details(request, pk):
    if request.user.is_authenticated:
        # Assuming only certain users are allowed to update resumes, such as candidates
        if request.user.is_applicant:
            resume = get_object_or_404(Resume, pk=pk, user=request.user)  # Ensure the resume belongs to the user
            if request.method == 'POST':
                form = UpdateResumeForm(request.POST, request.FILES, instance=resume)
                if form.is_valid():
                    form.save()
                    messages.info(request, 'Your resume has been updated')
                    return redirect('dashboard')
                else:
                    messages.warning(request, 'Something went wrong')
            else:
                form = UpdateResumeForm(instance=resume)
            context = {'form': form}
            return render(request, 'resume/update_resume.html', context)
        else:
            messages.warning(request, 'Permission Denied')
            return redirect('home')
    else:
        messages.warning(request, 'You must be logged in to update your resume')
        return redirect('login')