"""
Task 1: Web Scraping
Source: https://books.toscrape.com (practice site)
Output: data/books_raw.csv
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

Path("data").mkdir(exist_ok=True)

base_url = "https://books.toscrape.com/catalogue/page-{}.html"
books = []

for page in range(1, 4):  # scrape pages 1 to 3
    url = base_url.format(page)
    print("Scraping:", url)

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    for item in soup.select("article.product_pod"):
        title = item.h3.a["title"]
        price = item.select_one(".price_color").get_text(strip=True)
        rating = item.p.get("class", [None, None])[1]  # One, Two, Three...
        books.append({
            "title": title,
            "price": price,
            "rating": rating,
            "page": page,
        })

df = pd.DataFrame(books)
df.to_csv("data/books_raw.csv", index=False)

print(df.head())
print("Total rows:", len(df))
print("Saved: data/books_raw.csv")
