from django.urls import path
from . import views

urlpatterns = [
    path('', views.TemplateViewForm.as_view(), name='template_form'),
    path('all_transactions', views.all_transactions, name='all_transactions'),
]
