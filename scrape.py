import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.python.org/jobs/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

job_cards = soup.select("ol.list-recent-jobs li")

print("Cards Found:", len(job_cards))

jobs = []

for card in job_cards:

    # Title
    title_tag = card.select_one("h2 a")
    title = title_tag.get_text(strip=True) if title_tag else ""

    # Company
    company = ""
    company_tag = card.select_one(".listing-company-name")

    if company_tag:
        company_text = company_tag.get_text(" ", strip=True)

        # Remove title if it got mixed in
        if title and title in company_text:
            company_text = company_text.replace(title, "")

        # Remove "New" badge text
        company_text = company_text.replace("New", "").strip()

        company = company_text

    # Location
    location_tag = card.select_one(".listing-location")
    location = location_tag.get_text(strip=True) if location_tag else ""

    # Link
    link = ""
    if title_tag:
        href = title_tag.get("href", "")
        link = "https://www.python.org" + href

    jobs.append({
        "title": title,
        "company": company,
        "location": location,
        "link": link
    })

print("\nSample Jobs:")
for job in jobs[:5]:
    print(job)

with open("jobs.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "title",
            "company",
            "location",
            "link"
        ]
    )

    writer.writeheader()
    writer.writerows(jobs)

print(f"\nWrote {len(jobs)} rows to jobs.csv")