from django.views.generic import TemplateView, FormView
from .forms import EmployeeForm, EmployeeAgreementForm, UserRegistrationForm, UserLoginForm  # Assuming you have the EmployeeForm defined in forms.py
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from .forms import UserLoginForm
from django.contrib.auth.views import LogoutView


class HomePageView(TemplateView):
    template_name = 'home.html'


class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = UserRegistrationForm
    success_url = '/home'

    def form_valid(self, form):
        # Handle form submission logic, such as saving the data to the database
        form.save()
        return super().form_valid(form)


class LoginView(UserPassesTestMixin, FormView):
    template_name = 'login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('home')  # Use reverse_lazy for proper resolution of the home URL.

    def test_func(self):
        # Only allow access to unauthenticated users
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        # Redirect authenticated users trying to access login to the home page
        return redirect(self.success_url)

    def form_valid(self, form):
        # Get username and password from the form
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Authenticate the user
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            # Log the user in and redirect to success URL
            login(self.request, user)
            return super().form_valid(form)
        else:
            # Add error to the form if authentication fails
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)

    def get_success_url(self):
        return self.success_url


class CustomLogoutView(LoginRequiredMixin,LogoutView):
    next_page = reverse_lazy('home')


class EmployeeFormView(LoginRequiredMixin, FormView):
    template_name = 'onboarding_form.html'
    form_class = EmployeeForm
    success_url = '/home'  # Redirect to the home page after successful form submission
    permission_required = 'zentak_legal_automator.can_add_employee'  # Replace with your actual permission

    def form_valid(self, form):
        # Handle form submission logic, such as saving the data to the database
        form.save()
        return super().form_valid(form)


class EmployeeAgreementFormView(LoginRequiredMixin,FormView):
    template_name = 'pda1_request.html'
    form_class = EmployeeAgreementForm
    success_url = '/home'  # Redirect to the home page after successful form submission
    permission_required = 'zentak_legal_automator.can_add_employee_agreement'  # Replace with your actual permission

    def form_valid(self, form):
        # Handle form submission logic, such as saving the data to the database
        form.save()
        return super().form_valid(form)
