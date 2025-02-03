"""
URL configuration for admin_automator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from zentak_legal_automator.models import Employee, Department,Pda1
from django.contrib import admin
from django.urls import path, include
#admin.site.register(Employee)
#admin.site.register(Pda1)
#admin.site.register(Department)
# admin.site.register(User)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app_one/', include('zentak_legal_automator.urls')),  # Include app_one URLs
    #path('app_two/', include('zentak_leads_automator.urls')),  # Include app_two URLs
    path('app_three/', include('zentak_fintech_automator.urls')),
    path('app_four/', include('zentak_payroller_automator.urls')),
]
