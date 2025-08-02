import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

# === Step 1: Scrape data from DaAi TV ===
def scrape_daai_news(base_url, pages=1):
    scraped_data = []
    for page in range(1, pages+1):
        url = f"{base_url}?p={page}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}")
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract news items - adjust selectors based on the site structure
        news_items = soup.select('.history-list .item')  # Example CSS selector
        for item in news_items:
            date_text = item.select_one('.date').get_text(strip=True)  # e.g., "2025-01-01"
            event_text = item.select_one('.title').get_text(strip=True)  # News title
            detail_text = item.select_one('.description').get_text(strip=True) if item.select_one('.description') else ''
            
            full_text = f"{event_text}\n{detail_text}"
            
            # Convert date to YYYY-MM-DD format if needed
            match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', date_text)
            if match:
                year, month, day = match.groups()
                actual_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
                scraped_data.append({"Actual Date": actual_date, "Event": full_text})
    
    return scraped_data

base_url = "https://www.daai.tv/news/history"
scraped_data = scrape_daai_news(base_url, pages=10)  # Adjust number of pages if needed

# === Step 2: Load Excel File ===
file_path = '歷史的今天_內容統整.xlsx'
excel_data = pd.ExcelFile(file_path)
df_excel = pd.read_excel(file_path, sheet_name=excel_data.sheet_names[0])

# Extract events from Excel
excel_events = []
for _, row in df_excel.iterrows():
    for col in df_excel.columns[1:]:  # Skip '日期'
        event = row[col]
        if pd.notna(event):
            match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', event)
            if match:
                year, month, day = match.groups()
                actual_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
                excel_events.append({"Actual Date": actual_date, "Event": event.strip()})

# === Step 3: Combine scraped data and Excel data ===
combined_data = scraped_data + excel_events
combined_df = pd.DataFrame(combined_data)

# === Step 4: Sort and group by Month-Day ===
combined_df = combined_df.sort_values(by="Actual Date").reset_index(drop=True)
combined_df["Month-Day"] = combined_df["Actual Date"].apply(lambda x: x[5:])  # MM-DD format

grouped = combined_df.groupby("Month-Day")["Event"].apply(list).reset_index()

# Add bullet points
grouped["Events"] = grouped["Event"].apply(lambda evts: "\n".join([f"• {e}" for e in evts]))
grouped = grouped.drop(columns=["Event"])

# === Step 5: Export result ===
output_path = '/mnt/data/Combined_Grouped_Historical_Events.xlsx'
grouped.to_excel(output_path, index=False)
print(f"✅ Combined grouped data exported to: {output_path}")
