from django.db import models

class Attachment(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    file = models.FileField(upload_to='attachments/')
    from_email_address = models.EmailField()
    department = models.CharField(max_length=255)

    def __str__(self):
        return f"Attachment {self.id} from {self.from_email_address}"


class LoanShort(models.Model):
    id = models.AutoField(primary_key=True)
    borrower_first_name = models.CharField(max_length=255)
    borrower_last_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10)
    in_eur = models.DecimalField(max_digits=12, decimal_places=2)
    proof_document_file = models.FileField(upload_to='loans/')

    def __str__(self):
        return f"Loan for {self.borrower_first_name} {self.borrower_last_name}"


class Bonus(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    from_approver = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=50)
    department = models.CharField(max_length=255)

    def __str__(self):
        return f"Bonus for {self.first_name} {self.last_name}"


class HoursWorked(models.Model):
    emp_id = models.CharField(max_length=50)
    department = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    month = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f"Hours worked by {self.first_name} {self.last_name} in {self.month}/{self.year}"


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=255)
    department_short = models.CharField(max_length=50)
    contact_person_email = models.EmailField()
    partner = models.CharField(max_length=255)

    def __str__(self):
        return self.department


class AcceptanceProtocol(models.Model):
    id = models.AutoField(primary_key=True)
    partner = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    department_short = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    contact_person_email = models.EmailField()

    def __str__(self):
        return f"Protocol for {self.project_name}"


class ValueStream(models.Model):
    department = models.CharField(max_length=100)
    regex_pattern = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    contact_person_email = models.EmailField()

    def __str__(self):
        return self.subject