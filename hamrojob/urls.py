from django.urls import path
from . import views
from .views import HomeView, JobView, JobDetailView, ContactView, AboutView, JobSearchView, JobRecommendationsView
urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('job-list',JobView.as_view(),name='job-list'),
    path('job-detail/<int:pk>/',JobDetailView.as_view(),name='job-detail'),
    path('contact',ContactView.as_view(),name='contact'),
    path('about',AboutView.as_view(),name='about'),
    path('create-job/', views.create_job, name='create-job'),
    path('update-job/<int:pk>/', views.update_job, name='update-job'),
    path('manage-jobs/', views.manage_jobs, name='manage-jobs'),
    path('apply-to-job/<int:pk>/', views.apply_to_job, name='apply-to-job'),
    path('all-applicants/<int:pk>/', views.all_applicants, name='all-applicants'),
    path("job-search/", views.JobSearchView.as_view(), name="job-search"),
    path('applied-jobs/', views.applied_jobs, name="applied-jobs"),
    path('category/<int:category_id>/', views.JobListByCategoryView.as_view(), name='jobs-by-category'),
    path("recommendations/", JobRecommendationsView.as_view(), name="job-recommendations"),

]
