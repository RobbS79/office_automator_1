from django.views.generic import TemplateView, FormView, View
from .forms import EmployeeForm, Pda1RequestForm, UserRegistrationForm, UserLoginForm  # Assuming you have the EmployeeForm defined in forms.py
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from .forms import UserLoginForm
from django.contrib.auth.views import LogoutView
from .models import Employee, Pda1#, #EmployeeAgreement
from .pda1_filler_service.pdf_form_fields_editor import PDFFormFiller
from django.http import JsonResponse
from django.forms.models import model_to_dict


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


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Employee


from django.shortcuts import get_object_or_404, redirect
from django.http import FileResponse
from django.forms.models import model_to_dict
from .models import Employee, Pda1Doc, Pda1
from .pda1_filler_service.pdf_form_fields_editor import PDFFormFiller  # Assuming this handles PDF generation
import json

class EmployeesListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = "employees_list.html"
    context_object_name = "employees"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().order_by('zamestnanec_priezvisko')

from datetime import date

import json
import logging
from django.shortcuts import get_object_or_404, redirect
from django.forms.models import model_to_dict
from django.http import FileResponse
from datetime import date
from .models import Employee, Pda1, Pda1Doc
from .pda1_filler_service.pdf_form_fields_editor import PDFFormFiller  # Ensure the correct import path

# Configure logging
logger = logging.getLogger(__name__)

def generate_pdf(request, id_employee, id_employee_agreement):
    if request.method == "POST":
        try:
            # Fetch employee data
            employee = get_object_or_404(Employee, id_employee=id_employee)
            employee_data = model_to_dict(employee)

            # Fetch Pda1 data
            pda1 = get_object_or_404(Pda1, id_employee_agreement=id_employee_agreement)
            pda1_data = model_to_dict(pda1)

            # Merge dictionaries and handle non-serializable fields
            merged_data_dict = {**employee_data, **pda1_data}
            for key, value in merged_data_dict.items():
                if isinstance(value, date):
                    merged_data_dict[key] = value.isoformat()  # Convert dates to string

            # Convert to JSON for processing
            merged_json = json.dumps(merged_data_dict, indent=4)
            merged_dict = json.loads(merged_json)  # Convert back to dict

            logger.debug(f"Merged Data for PDF: {merged_dict}")

            # Fill the PDF
            form_filler_instance = PDFFormFiller(merged_dict)
            form_filler_instance.process_pda1_filler()

            # Check if PDF was generated
            file_path = form_filler_instance.pda1_form_output_path
            logger.debug(f"Generated PDF Path: {file_path}")

            # Ensure the file exists
            try:
                with open(file_path, 'rb') as f:
                    logger.info("PDF successfully generated.")
            except FileNotFoundError:
                logger.error(f"PDF not found at {file_path}")
                return redirect('error_page')  # Redirect to an error page if file missing

            # Save Pda1Doc record
            Pda1Doc.objects.create(
                id_employee=employee,
                file_path=file_path,
                file=form_filler_instance.pda1_form_output_path
            )

            # Return file as download response
            return FileResponse(open("/home/ubuntu/office_automator_1/admin_automator/zentak_legal_automator/pda1_filler_service/pdf_forms/filled_form.pdf", 'rb'), as_attachment=True, filename="Employee_Details.pdf")

        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}", exc_info=True)
            return redirect('error_page')  # Redirect to an error page in case of error

    logger.warning("Invalid request method for generate_pdf.")
    return redirect('app_one/home')


class Pda1FormView(LoginRequiredMixin,FormView):
    template_name = 'pda1_request.html'
    form_class = Pda1RequestForm
    success_url = 'app_one/home'  # Redirect to the home page after successful form submission
    permission_required = 'zentak_legal_automator.can_add_employee_agreement'  # Replace with your actual permission

    def form_valid(self, form):
        # Handle form submission logic, such as saving the data to the database
        form.save()
        return super().form_valid(form)
"""
    def post(self, request, *args, **kwargs):
        employees_qs = Employee.objects.all()
        emp_agreemnts_qs = EmployeeAgreement.objects.all()
        all_employees_data = []

        for index, obj in enumerate(employees_qs):
            if index > 0:
                break

            agreement_emp = emp_agreemnts_qs.filter(id_employee_agreement=obj.id_employee).first()
            if agreement_emp:
                agreement_emp_id = agreement_emp.id_employee_agreement
            else:
                # Handle case where no agreement was found
                agreement_emp_id = None

            employee_data = model_to_dict(obj)
            employee_json = {key: value for key, value in employee_data.items()}
            all_employees_data.append(employee_data)

            form_filler_instance = PDFFormFiller(employee_json)
            form_filler_instance.process_pda1_filler()

            # Assuming process_pda1_filler writes the form output to the following path:
            file_path = form_filler_instance.pda1_form_output_path  # Path to the generated PDF file

            # Create a new Pda1Doc record with the generated file path
            Pda1Doc.objects.create(
                id_employee=agreement_emp_id,
                file_path=file_path,
                #Try render pdf out of bytes
                file=form_filler_instance.pda1_form_output_path  # Store the file itself, if needed
            )

        # Redirect to another page after form submission
        return redirect('..')
"""

