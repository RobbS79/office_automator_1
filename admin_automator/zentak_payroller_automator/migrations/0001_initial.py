# Generated by Django 5.2a1 on 2025-02-08 11:52

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AcceptanceProtocol",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("partner", models.CharField(max_length=255)),
                ("project_name", models.CharField(max_length=255)),
                ("department_short", models.CharField(max_length=50)),
                ("price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("contact_person_email", models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name="Attachment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.DateField()),
                ("file", models.FileField(upload_to="attachments/")),
                ("from_email_address", models.EmailField(max_length=254)),
                ("department", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Bonus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("from_approver", models.CharField(max_length=255)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("unit", models.CharField(max_length=50)),
                ("department", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Department",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("department", models.CharField(max_length=255)),
                ("department_short", models.CharField(max_length=50)),
                ("contact_person_email", models.EmailField(max_length=254)),
                ("partner", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="HoursWorked",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("emp_id", models.CharField(max_length=50)),
                ("department", models.CharField(max_length=255)),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("month", models.IntegerField()),
                ("year", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="LoanShort",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("borrower_first_name", models.CharField(max_length=255)),
                ("borrower_last_name", models.CharField(max_length=255)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("currency", models.CharField(max_length=10)),
                ("in_eur", models.DecimalField(decimal_places=2, max_digits=12)),
                ("proof_document_file", models.FileField(upload_to="loans/")),
            ],
        ),
        migrations.CreateModel(
            name="ValueStream",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("department", models.CharField(max_length=100)),
                ("regex_pattern", models.CharField(max_length=255)),
                ("subject", models.CharField(max_length=100)),
                ("contact_person_email", models.EmailField(max_length=254)),
            ],
        ),
    ]
