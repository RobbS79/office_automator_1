# Generated by Django 5.2a1 on 2025-02-08 11:52

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Lead",
            fields=[
                ("lead_id", models.AutoField(primary_key=True, serialize=False)),
                ("headline", models.CharField(max_length=255)),
                ("description", models.TextField(default="not_defined", unique=True)),
                ("post_date", models.DateField()),
                ("value", models.CharField(blank=True, max_length=255, null=True)),
                ("customer_name", models.CharField(max_length=255)),
                (
                    "customer_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "customer_phone",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("location", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-post_date"],
            },
        ),
    ]
