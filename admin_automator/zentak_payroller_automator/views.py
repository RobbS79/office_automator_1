import pandas as pd
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .forms import AttachmentForm
from .models import HoursWorked, LoanShort, Attachment
from django.http import JsonResponse
#from .payroll_resources_service import category_processing_logic

# Views
class AttachmentCreateView(TemplateView):
    template_name = "attachment_form.html"

    def get(self, request, *args, **kwargs):
        form = AttachmentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/home')
        return render(request, self.template_name, {'form': form})


class PayrollResources(TemplateView):
    template_name = "payroll_resources.html"

    def get(self, request, *args, **kwargs):
        # Get queryset of Attachment
        all_attachments_qs = Attachment.objects.all()

        # Initialize attachment data
        attachment_data_processed = []

        # Check if attachments exist
        if all_attachments_qs.exists():
            for obj in all_attachments_qs:
                project = None
                print(f"Processing attachment: {obj.id}")
                print(f"Department: {obj.department}")

                if obj.department == "pragis - voda":
                    from .payroll_resources_service.hoursworked_processing_logic import pragis_voda_hours_worked
                    print("Calling pragis_voda_hours_worked...")
                    project = pragis_voda_hours_worked("hours_worked", str(obj.file),obj.date)

                elif obj.department == "pragis - stavba":
                    from .payroll_resources_service.hoursworked_processing_logic import pragis_stavba_hours_worked
                    print("Calling pragis_stavba_hours_worked...")
                    project = pragis_stavba_hours_worked("hours_worked", str(obj.file), obj.date)

                print("Project Result:", project)

                attachment_data = {
                    "id": obj.id,
                    "date": obj.date,
                    "file": obj.file.url if obj.file else None,
                    "file_view": project if isinstance(project, pd.DataFrame) else None,
                    "department": obj.department,
                }
                print(name for name in project.columns)
                """-- insert name as first_name and last_name to columns of
                -- zentak_payroller_automator_hoursworked
                -- id(name) as emp_id column, obj.department as department
                -- column, first_day.month as month column and first_day.year
                -- as year column
"""
                attachment_data_processed.append(attachment_data)
        else:
            print("No attachments exist.")

        return render(request, self.template_name, {"payroller_data": attachment_data_processed})

