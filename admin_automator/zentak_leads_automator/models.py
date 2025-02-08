from django.db import models

# Create your models here.

class Lead(models.Model):
    lead_id = models.AutoField(primary_key=True)
    headline = models.CharField(max_length=255)
    description = models.TextField(unique=True, default="not_defined")
    post_date = models.DateField()
    value = models.CharField(max_length=255, null=True, blank=True)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(null=True, blank=True)
    customer_phone = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.headline} - {self.customer_name}"

    class Meta:
        ordering = ['-post_date']
