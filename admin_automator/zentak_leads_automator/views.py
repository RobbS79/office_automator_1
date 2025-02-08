from django.http import JsonResponse
from django.shortcuts import render
from .playwright_service.playwright_nejstav_scraper_instance import NejstavScraper
from .models import Lead
from django.core import serializers
from datetime import datetime

def scraper_form(request):
    """Render the scraper form page"""
    return render(request, 'scraper_form.html')


def run_scraper(request):
    if request.method == "POST":
        try:
            scraper = NejstavScraper()
            leads_data = scraper.scrape()
            
            # Create Lead objects from the data
            leads_created = []
            for lead_dict in leads_data:
                # Convert date from "DD.MM.YYYY HH:MM" to "YYYY-MM-DD"
                try:
                    date_str = lead_dict['post_date']
                    if date_str:
                        date_obj = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
                        formatted_date = date_obj.strftime("%Y-%m-%d")
                    else:
                        formatted_date = None
                except ValueError:
                    print(f"Invalid date format: {date_str}")
                    formatted_date = None

                lead = Lead.objects.create(
                    headline=lead_dict['headline'],
                    description=lead_dict['description'],
                    post_date=formatted_date,  # Already formatted as YYYY-MM-DD
                    value=lead_dict['value'],
                    customer_name=lead_dict['customer_name'],
                    customer_email=lead_dict['customer_email'],
                    customer_phone=lead_dict['customer_phone'],
                    location=lead_dict['location']
                )
                leads_created.append(lead)
            
            # Convert leads to a list of dictionaries for JSON response
            leads_json = []
            for lead in leads_created:
                leads_json.append({
                    'headline': lead.headline,
                    'description': lead.description,
                    'post_date': lead.post_date,  # Already in correct format
                    'value': lead.value,
                    'customer_name': lead.customer_name,
                    'customer_email': lead.customer_email,
                    'customer_phone': lead.customer_phone,
                    'location': lead.location,
                    'created_at': lead.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return JsonResponse({
                "status": "Scraping completed!",
                "leads": leads_json
            })
            
        except Exception as e:
            import traceback
            return JsonResponse({
                "status": "Error",
                "message": str(e),
                "traceback": traceback.format_exc()
            }, status=500)
            
    return JsonResponse({"status": "Invalid request method. Use POST."})

    