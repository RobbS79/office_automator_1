from django.urls import path
from .views import (HomePageView, EmployeeFormView,
                    Pda1FormView, RegistrationView,
                    LoginView, CustomLogoutView, EmployeesListView,
                    generate_pdf)
#from .views import fill_pda1_form


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('home/', HomePageView.as_view(), name='home'),# Home page (landing page)
    path('onboarding/', EmployeeFormView.as_view(), name='onboarding_form'),
    path('pda1_request/', Pda1FormView.as_view(), name="pda1_request"),# Onboarding form page
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('employees/', EmployeesListView.as_view(), name='employees_list'),
    path('generate-pdf/<int:id_employee>/<int:id_employee_agreement>/', generate_pdf, name='generate_pdf'),
    #path('pda1_request/', FillPda1FormView.as_view(), name='pda1_request')
]
