from django.urls import path
from . import views
from .views import HomeView, JobView, JobDetailView, ContactView, AboutView
urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('job-list',JobView.as_view(),name='job-list'),
    path('job-detail/<int:pk>/',JobDetailView.as_view(),name='job-detail'),
    path('contact',ContactView.as_view(),name='contact'),
    path('about',AboutView.as_view(),name='about'),
    path('create-job/', views.create_job, name='create-job'),
    path('update-job/<int:pk>/', views.update_job, name='update-job')
]
