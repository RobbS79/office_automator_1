from django.urls import path
from . import views
from .views import LeadsListView, LeadDetailView, ConstructionProjectEstimateView

app_name = 'app_two'  # Define the namespace

urlpatterns = [
    path('', views.scraper_form, name='scraper-form'),
    path('run-scraper/', views.run_scraper, name='run-scraper'),
    path('leads/', LeadsListView.as_view(), name='leads_list'),
    path('leads/<int:lead_id>/', LeadDetailView.as_view(), name='lead_detail'),
    path('estimate/', ConstructionProjectEstimateView.as_view(), name='construction_project_estimate'),
]