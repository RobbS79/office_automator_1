from django.db import models


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)  # Automatically generates an ID field
    date = models.DateTimeField(null=False)  # DateTimeField for date and time
    amount = models.FloatField(null=False)  # FloatField for monetary values
    currency = models.CharField(max_length=10, null=False)  # CharField with max length for currency code
    transaction_type = models.CharField(max_length=50, null=False)  # Transaction type as string
    counterparty_bank_account = models.CharField(max_length=100, null=False)  # Account details
    message = models.TextField(null=False)  # TextField for potentially long messages
    category_1 = models.CharField(max_length=50, null=False)  # Main category
    category_2 = models.CharField(max_length=50, null=False)  # Subcategory

    class Meta:
        db_table = 'transactions'  # Explicitly set the table name

    def __str__(self):
        return f"Transaction {self.id} - {self.amount} {self.currency}"
