# File: scraping_to_db.py
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
import time

SUPABASE_URL = "<YOUR_SUPABASE_URL>"
SUPABASE_KEY = "<YOUR_SUPABASE_KEY>"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/?start={start}&type=2"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_listing_page(start: int):
    url = BASE_URL.format(start=start)
    print(f"Scraping page: {url}")
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')

    table_rows = soup.select("tr")
    all_data = []

    for row in table_rows[1:]:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        title_elem = cols[0].find("a")
        title = title_elem.text.strip()
        detail_url = title_elem['href']
        detail_url = f"https://www.shl.com{detail_url}" if not detail_url.startswith("http") else detail_url

        remote_testing = 'Yes' if cols[1].find(".green-dot") else 'No'
        adaptive = 'Yes' if cols[2].find(".green-dot") else 'No'
        test_type = cols[3].text.strip()

        details = scrape_detail_page(detail_url)

        data = {
            "title": title,
            "detail_url": detail_url,
            "remote_testing": remote_testing,
            "adaptive": adaptive,
            "test_type": test_type,
            "assessment_length": details["length"],
            "info_blob": details["blob"]
        }

        all_data.append(data)

    return all_data

def scrape_detail_page(url):
    time.sleep(1)
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')

    def extract_text(selector):
        section = soup.select_one(selector)
        return section.get_text(strip=True) if section else ""

    desc = extract_text(".shl-content h2:contains('Description') + p")
    job_level = extract_text(".shl-content h2:contains('Job levels') + p")
    lang = extract_text(".shl-content h2:contains('Languages') + p")
    length = extract_text(".shl-content h2:contains('Assessment length') + p")

    blob = f"Description: {desc}\nJob Levels: {job_level}\nLanguages: {lang}"
    return {"length": length, "blob": blob}

def upload_to_supabase(records):
    for rec in records:
        response = supabase.table("assessments").insert(rec).execute()
        print(response)

if __name__ == "__main__":
    all_records = []
    for start in range(0, 12 * 12, 12):  # pages at intervals of 12
        records = scrape_listing_page(start)
        all_records.extend(records)

        with open("scraped_output.txt", "a", encoding="utf-8") as f:
            for rec in records:
                f.write(str(rec) + "\n")

        upload_to_supabase(records)
