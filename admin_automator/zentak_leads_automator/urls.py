from django.urls import path
from . import views

app_name = 'app_two'  # Add namespace

urlpatterns = [
    path('', views.scraper_form, name='scraper-form'),
    path('run-scraper/', views.run_scraper, name='run-scraper'),
]