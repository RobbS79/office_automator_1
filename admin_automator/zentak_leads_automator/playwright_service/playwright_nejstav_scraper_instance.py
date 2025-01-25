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
    def __init__(self, url, executable_path, db_path="db.sqlite3"):
        self.url = url
        self.executable_path = executable_path
        self.db_path = db_path
        self.browser = None
        self.page = None
        self.leads_df = pd.DataFrame()

    def login(self):
        """Logs into the website using credentials from environment variables."""
        self.page.wait_for_selector("xpath=/html/body/div[1]/header/div/div[2]/a[5]").click()
        time.sleep(2)
        self.page.wait_for_selector("xpath=/html/body/div[1]/div[1]/div/div[2]/div/form/div[1]/label[2]/input").fill(
            os.getenv("USERNAME")
        )
        self.page.wait_for_selector("xpath=/html/body/div[1]/div[1]/div/div[2]/div/form/div[2]/label[2]/input").fill(
            os.getenv("PASSWORD")
        )
        self.page.wait_for_selector("xpath=/html/body/div[1]/div[1]/div/div[2]/div/form/button").click()
        time.sleep(3)

    def get_demand_details(self):
        """Extracts details of a specific demand from the page."""
        lead_dict = {}
        url = self.page.url

        # Extract the digits after the third '/' and before the '-'
        match = re.search(r'/prace/(\d+)-', url)
        project_id = match.group(1) if match else None

        headline = self.page.wait_for_selector("xpath=/html/body/div[1]/div[1]/div[1]/div[1]/div/div[2]/h1").inner_text()
        description_element = self.page.wait_for_selector("xpath=/html/body/div[1]/div[1]/div[1]/div[1]/div").query_selector_all("p")
        description_string = "".join([p.inner_text() for p in description_element if len(p.inner_text()) > 2])
        post_date = self.page.wait_for_selector("xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/ul/li[1]/strong").inner_text()
        value = self.page.wait_for_selector("xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/ul/li[4]/strong").inner_text()

        try:
            customer_name = self.page.wait_for_selector("xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div/ul/li[1]/strong").inner_text()
        except TimeoutError:
            customer_name, customer_email, customer_phone, location = "null", "null", "null", "null"
            self.page.go_back()
            return None

        customer_email = self._safe_selector("xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div/ul/li[3]/a", default="unknown")
        customer_phone = self._safe_selector("xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div/ul/li[4]/a", default="unknown")
        location = self._safe_selector("xpath=/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/ul/li[3]/strong", default="unknown")

        lead_dict[project_id] = {
            "id": project_id,
            "headline": headline,
            "description": description_string,
            "post_date": post_date,
            "value": value,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_phone": customer_phone,
            "location": location,
        }

        self.page.go_back()
        print(f"Finished: {project_id}")
        return lead_dict

    def _safe_selector(self, xpath, default=""):
        """Handles safe selection with a timeout."""
        try:
            return self.page.wait_for_selector(xpath).inner_text()
        except TimeoutError:
            return default

    def scrape(self):
        """Main method to scrape the demands."""
        with sync_playwright() as p:
            self.browser = p.chromium.launch_persistent_context(
                user_data_dir="",  # Optional: Provide a user data directory
                executable_path=self.executable_path,  # Explicitly use Chrome
                headless=False,
            )
            self.page = self.browser.new_page()
            self.page.goto(self.url)
            time.sleep(3)

            # Accept cookies
            self.page.wait_for_selector("xpath=/html/body/div[3]/div/div[2]/div/button[2]").click()

            # Log in
            self.login()

            # Locate all demand elements
            list_of_demands = self.page.wait_for_selector("xpath=/html/body/div[1]/div[3]")
            concrete_div_elements = list_of_demands.query_selector_all(".w-full.mb-8")

            # Iterate through demands
            for i in range(len(concrete_div_elements)):
                element = concrete_div_elements[i]
                element.click()
                dict_output = self.get_demand_details()
                if dict_output:
                    temp_df = pd.DataFrame(data=dict_output.values())
                    self.leads_df = pd.concat([self.leads_df, temp_df], ignore_index=True)
                    time.sleep(3)

            self.browser.close()
        return self.leads_df

    def save_to_sql(self, table_name="leads"):
        """Save the collected DataFrame to an SQLite database."""
        conn = sqlite3.connect(self.db_path)
        self.leads_df.to_sql(name=table_name, con=conn, if_exists="append", index=False)
        conn.close()

    def save_to_excel(self, filename="new_leads.xlsx"):
        """Save the collected DataFrame to an Excel file."""
        self.leads_df.to_excel(filename, index=False)


# Usage
url = "https://nejstav.cz/katalog-praci?filters%5Bcategory%5D%5B%5D=65&filters%5Bcategory%5D%5B%5D=3&filters%5Bcategory%5D%5B%5D=1&filters%5Bcategory%5D%5B%5D=59&filters%5Bcategory%5D%5B%5D=23&filters%5Bcategory%5D%5B%5D=115&filters%5Bcategory%5D%5B%5D=27&filters%5Bcategory%5D%5B%5D=95&filters%5Bcategory%5D%5B%5D=11&filters%5Bcategory%5D%5B%5D=5&filters%5Bcategory%5D%5B%5D=63&filters%5Bcategory%5D%5B%5D=81&filters%5Bregion%5D%5B%5D=1&filters%5Bquery%5D="
executable_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

scraper = NejstavScraper(url, executable_path)
df = scraper.scrape()
scraper.save_to_sql()
scraper.save_to_excel()

print("Scraping completed!")
