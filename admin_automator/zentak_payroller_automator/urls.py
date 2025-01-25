from django.urls import path
from .views import AttachmentCreateView, PayrollResources
#from django.views.generic import TemplateView


urlpatterns = [
    #path('', HomePageView.as_view(), name='home'),  # Home page (landing page)
    path('attachement_form/', AttachmentCreateView.as_view(), name='attachement_form'),
    path('hours-worked/', PayrollResources.as_view(), name='payroll_resources')
]