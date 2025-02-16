from playwright.sync_api import sync_playwright
import pandas as pd
import json

class PriceIndicatorCursor:
    def __init__(self):
        self.url = "https://www.cenikyremesel.cz/cenik-stavebnich-praci"
        self.data = []
        
    def fetch_data(self):
        try:
            with sync_playwright() as p:
                print("Launching browser...")
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                page.set_viewport_size({"width": 1920, "height": 1080})
                
                print(f"Navigating to {self.url}")
                page.goto(self.url)
                page.wait_for_load_state('networkidle')
                page.wait_for_timeout(5000)
                
                # Accept cookies if present
                try:
                    print("Checking for cookie consent...")
                    page.wait_for_selector('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll', 
                                         timeout=5000)
                    page.click('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
                    print("Accepted cookies")
                    page.wait_for_timeout(2000)
                except:
                    print("No cookie consent found or already accepted")
                
                print("Processing table data...")
                processed_data = {}
                empty_runs = 0
                processed_row_positions = set()
                
                # Predefined column names
                columns = [
                    "Profese",
                    "Kategorie",
                    "Popis práce",
                    "Popis materiálu",
                    "mj",
                    "Cena práce pro řemeslníka",
                    "Cena práce pro stavební firmu (+35%)",
                    "Cena nákupu materiálu",
                    "Cena prodeje materiálu (+15%)",
                    "Váha materiálu",
                    "Odpad suť"
                ]
                
                while empty_runs < 8:
                    # Wait for table content to be stable
                    page.wait_for_timeout(3000)
                    
                    # Get all rows with their positions
                    rows_info = page.evaluate("""() => {
                        const rows = Array.from(document.querySelectorAll('table tbody tr'));
                        const viewport_top = window.scrollY;
                        const viewport_height = window.innerHeight;
                        
                        return rows.map(row => {
                            const rect = row.getBoundingClientRect();
                            return {
                                position: rect.top + window.scrollY,
                                visible: rect.top >= -200 && rect.bottom <= viewport_height + 200,
                                isFirst: row.parentElement.firstElementChild === row,
                                category: row.parentElement.firstElementChild.textContent.trim()
                            };
                        });
                    }""")
                    
                    current_position = page.evaluate('window.scrollY')
                    document_height = page.evaluate('document.documentElement.scrollHeight')
                    
                    visible_rows = [r for r in rows_info if r['visible']]
                    unprocessed_positions = [
                        r['position'] for r in visible_rows 
                        if r['position'] not in processed_row_positions
                    ]
                    
                    print(f"Current scroll: {current_position}/{document_height}")
                    print(f"Total rows: {len(rows_info)}")
                    print(f"Visible rows: {len(visible_rows)}")
                    print(f"Unprocessed visible rows: {len(unprocessed_positions)}")
                    
                    if not unprocessed_positions:
                        scroll_amount = 300
                        new_position = current_position + scroll_amount
                        page.evaluate(f'window.scrollTo(0, {new_position})')
                        print(f"No unprocessed rows, scrolling to {new_position}")
                        page.wait_for_timeout(8000)
                        empty_runs += 1
                        print(f"Empty run {empty_runs}/8")
                        continue
                    
                    # Process visible tbody sections
                    new_rows = 0
                    
                    for tbody in page.query_selector_all('table tbody'):
                        rows = tbody.query_selector_all('tr')
                        if not rows:
                            continue
                            
                        # Get category (Profese) from first row
                        category_row = rows[0]
                        category = category_row.text_content().strip()
                        if not category:
                            continue
                            
                        # Initialize category in processed_data if not exists
                        if category not in processed_data:
                            processed_data[category] = []
                            
                        # Process data rows
                        for data_row in rows[1:]:
                            # Get row position
                            row_position = data_row.evaluate("""(row) => {
                                const rect = row.getBoundingClientRect();
                                return rect.top + window.scrollY;
                            }""")
                            
                            if row_position in processed_row_positions:
                                continue
                                
                            # Check visibility
                            is_visible = data_row.evaluate("""(row) => {
                                const rect = row.getBoundingClientRect();
                                return rect.top >= -200 && rect.bottom <= window.innerHeight + 200;
                            }""")
                            
                            if not is_visible:
                                continue
                                
                            cells = data_row.query_selector_all('td')
                            if len(cells) != 11:
                                continue
                                
                            values = [cell.text_content().strip() for cell in cells]
                            
                            row_dict = {
                                columns[0]: category,  # Category becomes Profese
                                columns[1]: values[0],
                                columns[2]: values[1],
                                columns[3]: values[2],
                                columns[4]: values[3],
                                columns[5]: values[4],
                                columns[6]: values[5],
                                columns[7]: values[6],
                                columns[8]: values[7],
                                columns[9]: values[8],
                                columns[10]: values[9]
                            }
                            
                            # Add to category array
                            if row_dict not in processed_data[category]:
                                processed_data[category].append(row_dict)
                                new_rows += 1
                                processed_row_positions.add(row_position)
                                print(f"Added new row at position {row_position}:")
                                print(f"  Category: {category}")
                                print(f"  Kategorie: {values[0]}")
                                print(f"  Popis práce: {values[1]}")
                                print(f"  Popis materiálu: {values[2]}")
                                print(f"  mj: {values[3]}")
                                print(f"  Cena práce pro řemeslníka: {values[4]}")
                                print(f"  Cena práce pro stavební firmu: {values[5]}")
                                print(f"  Cena nákupu materiálu: {values[6]}")
                                print(f"  Cena prodeje materiálu: {values[7]}")
                                print(f"  Váha materiálu: {values[8]}")
                                print(f"  Odpad suť: {values[9]}")
                                print("---")
                    
                    total_processed = sum(len(rows) for rows in processed_data.values())
                    print(f"Processed {new_rows} new rows in this batch")
                    print(f"Total categories: {len(processed_data)}")
                    print(f"Total processed rows: {total_processed}")
                    
                    if new_rows > 0:
                        # Scroll to just after the last processed row
                        next_position = max(processed_row_positions) + 100
                        page.evaluate(f'window.scrollTo(0, {next_position})')
                        print(f"Scrolled to position {next_position}")
                        page.wait_for_timeout(8000)
                        empty_runs = 0
                    else:
                        empty_runs += 1
                        print(f"No new rows found. Empty run {empty_runs}/8")
                        page.evaluate('window.scrollBy(0, 300)')
                        page.wait_for_timeout(8000)
                
                print(f"Scraping completed. Total categories: {len(processed_data)}")
                print(f"Total records: {sum(len(records) for records in processed_data.values())}")
                
                if processed_data:
                    self.data = processed_data
                    return processed_data
                    
                return None
                
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return None

    def save_to_json(self, filename="construction_prices.json"):
        if not self.data or len(self.data) == 0:  # Better empty check
            print("No data to save")
            return False
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            print(f"Data successfully saved to {filename}")
            print(f"Total categories saved: {len(self.data)}")
            total_records = sum(len(records) for records in self.data.values())
            print(f"Total records saved: {total_records}")
            return True
        except Exception as e:
            print(f"Error saving data to JSON: {str(e)}")
            return False

def main():
    scraper = PriceIndicatorCursor()
    data = scraper.fetch_data()
    if data:
        scraper.save_to_json()
    else:
        print("Scraping failed - no data to save")

if __name__ == "__main__":
    main()
