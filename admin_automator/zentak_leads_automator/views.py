"""from django.http import JsonResponse
from .playwright_service.playwright_nejstav_scraper_instance import NejstavScraper

def run_scraper(request):
    if request.method == "POST":  # Only allow POST requests
        scraper = NejstavScraper()
        leads_df = scraper.run()
        leads = leads_df.to_dict(orient="records")  # Convert DataFrame to list of dictionaries
        return JsonResponse({"status": "Scraping completed!", "leads": leads}, safe=False)
    return JsonResponse({"status": "Invalid request method. Use POST."})
"""