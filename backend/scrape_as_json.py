
import requests
from bs4 import BeautifulSoup
import time
import os
import json

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
    print(f"Scraping detail page: {url}")
    time.sleep(1)
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')

    def extract_text_by_heading(heading):
        # Look for all .row divs, then h4 with the heading, then next <p>
        for row_div in soup.select(".row"):
            h4 = row_div.find("h4")
            if h4 and heading.lower() in h4.get_text(strip=True).lower():
                p = h4.find_next_sibling("p")
                if p:
                    return p.get_text(strip=True)
        return ""

    desc = extract_text_by_heading("Description")
    job_level = extract_text_by_heading("Job levels")
    lang = extract_text_by_heading("Languages")
    length = extract_text_by_heading("Assessment length")

    blob = f"Description: {desc}\nJob Levels: {job_level}\nLanguages: {lang}"
    return {"length": length, "blob": blob}

def save_jsonl(records, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        for rec in records:
            json.dump(rec, f, ensure_ascii=False)
            f.write("\n")

if __name__ == "__main__":
    all_records = []
    for start in range(0, 12 * 12, 12):  # pages at intervals of 12
        records = scrape_listing_page(start)
        all_records.extend(records)
    save_jsonl(all_records, os.path.join("context", "scraped_data.jsonl"))
    print(f"Saved {len(all_records)} records to context/scraped_data.jsonl")
