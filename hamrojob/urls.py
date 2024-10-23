from django.contrib import admin
from django.urls import path
from .views import HomeView, JobView, JobDetailView, ContactView, AboutView
urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('job-list',JobView.as_view(),name='job-list'),
    path('job-detail',JobDetailView.as_view(),name='job-detail'),
    path('contact',ContactView.as_view(),name='contact'),
    path('about',AboutView.as_view(),name='about'),

]