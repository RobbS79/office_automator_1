from django.shortcuts import render

# Create your views here.

"""-- create TemplateViewForm which will at url provide a button to run
-- fintech_service package at current_django_app_path/fintech_service
-- as output it will direct to path sqlite_db_name/all_transactions
-- showing django.models objects.all. I have fintech_service already 
-- prepared and it outputs pandas dataframe. Return a code for views.py"""

import os
import pandas as pd
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .models import Transaction


# Path to the fintech_service
FINTECH_SERVICE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fintech_service')


# Dummy function to simulate the fintech_service output (Replace with actual service call)

# View to render the template with button
class TemplateViewForm(TemplateView):
    template_name = 'get_transactions_categorised.html'  # Replace with the actual template path
    def __init__(self):
        from .fintech_service.transactions_categorisation.csob_transactions_categorisation_lvl_2 import ExpenseCategorisationLvl2
        self.lvl2_cat_instance = ExpenseCategorisationLvl2(
                    os.path.join(FINTECH_SERVICE_PATH, '/Users/robertsoroka/PycharmProjects/office_automator_1/admin_automator/zentak_fintech_automator/fintech_service/transactions_categorisation/category_1.csv'),
                    os.path.join(FINTECH_SERVICE_PATH, '/Users/robertsoroka/PycharmProjects/office_automator_1/admin_automator/zentak_fintech_automator/fintech_service/transactions_categorisation/init_transactions_mapper.json'))
    def post(self, request, *args, **kwargs):
        # Trigger fintech service and get the pandas dataframe
        df = self.lvl2_cat_instance.assign_category_2_using_data_dict()

        # Insert data into Django model (Database)
        for _, row in df.iterrows():
            Transaction.objects.create(
                #id=row['id'],
                date=row['Date'],
                amount=row['Amount'],
                currency=row['Currency'],
                transaction_type=row['Transaction Type'],
                counterparty_bank_account=row['Counterparty bank account'],
                message=row['Message'],
                category_1=row['category_1'],
                category_2=row['category_2']
            )

        # Redirect to view the transactions
        return HttpResponseRedirect('/all_transactions')


# View to show all transactions
def all_transactions(request):
    transactions = Transaction.objects.all()  # Get all transactions
    return render(request, 'all_transactions.html', {'transactions': transactions})

