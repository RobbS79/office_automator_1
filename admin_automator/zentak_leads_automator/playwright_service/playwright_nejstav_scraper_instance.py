from playwright.sync_api import sync_playwright
from playwright._impl._errors import TimeoutError
import time
import os
import re
import pandas as pd
import sqlite3
from dotenv import load_dotenv

load_dotenv()


class NejstavScraper:
    def __init__(self):
        self.url = "https://nejstav.cz/katalog-praci?filters%5Bcategory%5D%5B%5D=65&filters%5Bcategory%5D%5B%5D=3&filters%5Bcategory%5D%5B%5D=1&filters%5Bcategory%5D%5B%5D=59&filters%5Bcategory%5D%5B%5D=23&filters%5Bcategory%5D%5B%5D=115&filters%5Bcategory%5D%5B%5D=27&filters%5Bcategory%5D%5B%5D=95&filters%5Bcategory%5D%5B%5D=11&filters%5Bcategory%5D%5B%5D=5&filters%5Bcategory%5D%5B%5D=63&filters%5Bcategory%5D%5B%5D=81&filters%5Bregion%5D%5B%5D=1&filters%5Bquery%5D="
        self.executable_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.browser = None
        self.page = None
        self.leads_list = []

    def initialize_browser(self):
        """Initialize browser and new page"""
        self.browser = self.playwright.chromium.launch_persistent_context(
            user_data_dir="",
            executable_path=self.executable_path,
            headless=False,
        )
        self.page = self.browser.new_page()

    def handle_cookies(self):
        """Handle cookie consent"""
        try:
            cookie_button = self.page.wait_for_selector("xpath=/html/body/div[3]/div/div[2]/div/button[2]")
            cookie_button.click()
            time.sleep(1)
        except TimeoutError:
            print("Cookie consent button not found or already accepted")

    def login(self):
        """Handle login process"""
        try:
            # Click login button
            self.page.wait_for_selector("xpath=/html/body/div[1]/header/div/div[2]/a[5]").click()
            time.sleep(2)

            # Get credentials from environment variables
            username = os.getenv("NEJSTAV_USERNAME")  # Changed from USERNAME
            password = os.getenv("NEJSTAV_PASSWORD")  # Changed from PASSWORD

            # Verify credentials are available
            if not username or not password:
                raise ValueError("Missing credentials in environment variables. Please set NEJSTAV_USERNAME and NEJSTAV_PASSWORD")

            # Fill credentials
            self.page.wait_for_selector(
                "xpath=/html/body/div[1]/div[1]/div/div[2]/div/form/div[1]/label[2]/input"
            ).fill(username)
            
            self.page.wait_for_selector(
                "xpath=/html/body/div[1]/div[1]/div/div[2]/div/form/div[2]/label[2]/input"
            ).fill(password)

            # Submit login
            self.page.wait_for_selector(
                "xpath=/html/body/div[1]/div[1]/div/div[2]/div/form/button"
            ).click()
            time.sleep(3)
            
        except TimeoutError as e:
            print(f"Login failed: {str(e)}")
            raise
        except ValueError as e:
            print(f"Credential error: {str(e)}")
            raise

    def get_demand_details(self):
        """Extract details from a single demand page"""
        try:
            url = self.page.url
            match = re.search(r'/prace/(\d+)-', url)
            project_id = match.group(1) if match else None

            selectors = {
                'headline': "xpath=/html/body/div[1]/div[1]/div[1]/div[1]/div/div[2]/h1",
                'description': "xpath=/html/body/div[1]/div[1]/div[1]/div[1]/div",
                'post_date': "xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/ul/li[1]/strong",
                'value': "xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/ul/li[4]/strong",
                'customer_name': "xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div/ul/li[1]/strong",
                'customer_email': "xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div/ul/li[3]/a",
                'customer_phone': "xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div/ul/li[4]/a",
                'location': "xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/ul/li[3]/strong"
            }

            lead_dict = {
                'id': project_id,
                'headline': self._get_text(selectors['headline']),
                'description': self._get_description(selectors['description']),
                'post_date': self._get_text(selectors['post_date']),
                'value': self._get_text(selectors['value']),
                'customer_name': self._get_text(selectors['customer_name']),
                'customer_email': self._get_text(selectors['customer_email'], "unknown"),
                'customer_phone': self._get_text(selectors['customer_phone'], "unknown"),
                'location': self._get_text(selectors['location'], "unknown")
            }

            return lead_dict

        except Exception as e:
            print(f"Error extracting demand details: {str(e)}")
            return None
        finally:
            self.page.go_back()

    def _get_text(self, selector, default=""):
        """Safely get text from a selector"""
        try:
            element = self.page.wait_for_selector(selector)
            return element.inner_text() if element else default
        except TimeoutError:
            return default

    def _get_description(self, selector):
        """Get description text from multiple p elements"""
        try:
            description_element = self.page.wait_for_selector(selector)
            p_elements = description_element.query_selector_all("p")
            return "".join([p.inner_text() for p in p_elements if len(p.inner_text()) > 2])
        except TimeoutError:
            return ""

    def collect_leads(self):
        """Collect all leads from the page"""
        try:
            # Wait for the page to be fully loaded
            self.page.wait_for_load_state('networkidle')
            time.sleep(2)
            
            # Get all hrefs first
            self.page.wait_for_selector("div.w-full.mb-8 a")
            lead_elements = self.page.query_selector_all("div.w-full.mb-8 a")
            
            # Store all URLs before processing
            lead_urls = []
            for element in lead_elements:
                try:
                    href = element.get_attribute('href')
                    if href:
                        if href.startswith('http'):
                            lead_urls.append(href)
                        else:
                            href = href.lstrip('/')
                            lead_urls.append(f"https://nejstav.cz/{href}")
                except Exception as e:
                    print(f"Error getting href: {e}")
                    continue
            
            print(f"Found {len(lead_urls)} leads to process")
            
            # Process each URL
            for i, url in enumerate(lead_urls, 1):
                try:
                    print(f"Processing lead {i}/{len(lead_urls)}: {url}")
                    
                    # Navigate to detail page
                    self.page.goto(url)
                    self.page.wait_for_load_state('networkidle')
                    time.sleep(2)
                    
                    lead_data = self.extract_lead_details()
                    if lead_data:
                        self.leads_list.append(lead_data)
                        print(f"Successfully collected lead: {lead_data.get('headline', 'Unknown')}")
                    
                    # Return to list page
                    self.page.goto(self.url)
                    self.page.wait_for_load_state('networkidle')
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Error processing lead {i}: {str(e)}")
                    self.page.goto(self.url)
                    self.page.wait_for_load_state('networkidle')
                    time.sleep(2)
                    continue
                
        except Exception as e:
            print(f"Error collecting leads: {str(e)}")
            raise

    def extract_lead_details(self):
        """Extract details from the current detail page"""
        try:
            # Wait for main content to load
            self.page.wait_for_selector("xpath=/html/body/div[1]/div[1]/div[1]/div[1]/div/div[2]/h1")
            
            # Get project ID from URL
            url = self.page.url
            match = re.search(r'/prace/(\d+)-', url)
            project_id = match.group(1) if match else ""
            
            # Get headline
            headline = self.page.locator("xpath=/html/body/div[1]/div[1]/div[1]/div[1]/div/div[2]/h1").inner_text()
            
            # Get description
            description_elements = self.page.locator("xpath=/html/body/div[1]/div[1]/div[1]/div[1]/div").locator("p").all()
            description = " ".join([elem.inner_text() for elem in description_elements if elem.inner_text().strip()])
            
            # Get metadata from first ul
            metadata_items = self.page.locator("xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/ul").locator("li").all()
            post_date = metadata_items[0].locator("strong").inner_text() if len(metadata_items) > 0 else ""
            location = metadata_items[2].locator("strong").inner_text() if len(metadata_items) > 2 else ""
            value = metadata_items[3].locator("strong").inner_text() if len(metadata_items) > 3 else ""
            
            # Get contact info from second ul
            contact_items = self.page.locator("xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div/ul").locator("li").all()
            customer_name = contact_items[0].locator("strong").inner_text() if len(contact_items) > 0 else ""
            customer_email = contact_items[2].locator("a").inner_text() if len(contact_items) > 2 else ""
            customer_phone = contact_items[3].locator("a").inner_text() if len(contact_items) > 3 else ""
            
            lead_data = {
                'id': project_id,
                'headline': headline.strip(),
                'description': description.strip(),
                'post_date': post_date.strip(),
                'value': value.strip(),
                'customer_name': customer_name.strip(),
                'customer_email': customer_email.strip(),
                'customer_phone': customer_phone.strip(),
                'location': location.strip()
            }
            
            print(f"Extracted lead data: {lead_data['headline']}")
            return lead_data
            
        except Exception as e:
            print(f"Error extracting lead details: {str(e)}")
            return None

    def create_dataframe(self):
        """Convert collected leads to list of dictionaries"""
        try:
            if not self.leads_list:
                return []

            # Create a list of dictionaries with consistent data
            cleaned_data = []
            for lead in self.leads_list:
                row = {
                    'id': str(lead.get('id', '')),
                    'headline': str(lead.get('headline', '')),
                    'description': str(lead.get('description', '')),
                    'post_date': str(lead.get('post_date', '')),
                    'value': str(lead.get('value', '')),
                    'customer_name': str(lead.get('customer_name', '')),
                    'customer_email': str(lead.get('customer_email', '')),
                    'customer_phone': str(lead.get('customer_phone', '')),
                    'location': str(lead.get('location', ''))
                }
                cleaned_data.append(row)
            
            return cleaned_data
            
        except Exception as e:
            print(f"Error creating data structure: {str(e)}")
            return []

    def scrape(self):
        """Main scraping method"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080}
                )
                self.page = context.new_page()
                
                try:
                    # Navigate to the main page
                    print("Navigating to the main page...")
                    self.page.goto(self.url)
                    self.page.wait_for_load_state('networkidle')
                    time.sleep(3)

                    print("Handling cookies...")
                    self.handle_cookies()
                    
                    print("Logging in...")
                    self.login()

                    print("Collecting leads...")
                    self.collect_leads()
                    
                finally:
                    context.close()
                    browser.close()

            print(f"Scraping completed. Collected {len(self.leads_list)} leads")
            return self.leads_list

        except Exception as e:
            print(f"Scraping failed: {e}")
            return []

    def save_to_sql(self, table_name="leads"):
        """Save the collected DataFrame to an SQLite database."""
        conn = sqlite3.connect("db.sqlite3")
        df = pd.DataFrame(self.leads_list)
        df.to_sql(name=table_name, con=conn, if_exists="append", index=False)
        conn.close()

    def save_to_excel(self, filename="new_leads.xlsx"):
        """Save the collected DataFrame to an Excel file."""
        df = pd.DataFrame(self.leads_list)
        df.to_excel(filename, index=False)


# Usage
"""url = "https://nejstav.cz/katalog-praci?filters%5Bcategory%5D%5B%5D=65&filters%5Bcategory%5D%5B%5D=3&filters%5Bcategory%5D%5B%5D=1&filters%5Bcategory%5D%5B%5D=59&filters%5Bcategory%5D%5B%5D=23&filters%5Bcategory%5D%5B%5D=115&filters%5Bcategory%5D%5B%5D=27&filters%5Bcategory%5D%5B%5D=95&filters%5Bcategory%5D%5B%5D=11&filters%5Bcategory%5D%5B%5D=5&filters%5Bcategory%5D%5B%5D=63&filters%5Bcategory%5D%5B%5D=81&filters%5Bregion%5D%5B%5D=1&filters%5Bquery%5D="
executable_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

scraper = NejstavScraper()
df = scraper.scrape()
scraper.save_to_sql()
scraper.save_to_excel()

print("Scraping completed!")
"""