from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('headline', 'customer_name', 'post_date', 'value', 'location')
    search_fields = ('headline', 'customer_name', 'description')
    list_filter = ('post_date', 'location')
