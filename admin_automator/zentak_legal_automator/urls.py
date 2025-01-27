from django.urls import path
from .views import HomePageView, EmployeeFormView, EmployeeAgreementFormView, RegistrationView, LoginView, CustomLogoutView
from .views import fill_pda1_form

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('home/', HomePageView.as_view(), name='home'),# Home page (landing page)
    path('onboarding/', EmployeeFormView.as_view(), name='onboarding_form'),
    path('pda1_request', EmployeeAgreementFormView.as_view(), name="pda1_request"),# Onboarding form page
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('fill-pda1-form/', fill_pda1_form, name='fill_pda1_form'),
]
