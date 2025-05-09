# web-data-scraper.py

import argparse
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, urljoin

def fetch_html(url, delay, save, page_number):
    print(f"Fetching: {url}")
    time.sleep(delay)
    response = requests.get(url)
    html_text = response.text
    if save:
        with open(f"page_{page_number}.html", "w", encoding="utf-8") as file:
            file.write(html_text)
    return html_text

def extract_links_from_html(html_text, link_class, base_domain):
    soup = BeautifulSoup(html_text, "lxml")
    links = soup.find_all("a", class_=link_class, href=True)
    full_links = [urljoin(base_domain, link["href"]) for link in links]
    return full_links

def main():
    parser = argparse.ArgumentParser(description="Scrape listing links from paginated HTML pages.")
    parser.add_argument("url", type=str, help="Base URL without pagination (e.g., https://example.com/listings)")
    parser.add_argument("pagination", type=str, help="Pagination query key (e.g., page, stranka)")
    parser.add_argument("link_class", type=str, help="Class name of anchor tags to extract (e.g., listing-item)")
    parser.add_argument("--pages", type=int, default=276, help="Number of pages to scrape (default: 276)")
    parser.add_argument("--delay", type=int, default=5, help="Delay between requests (default: 5s)")
    parser.add_argument("--output", type=str, default="output_links.csv", help="Output CSV file name")
    parser.add_argument("--no-save", action="store_true", help="Do not save HTML files")

    args = parser.parse_args()
    base_domain = f"{urlparse(args.url).scheme}://{urlparse(args.url).netloc}"

    all_links = []
    for i in range(1, args.pages + 1):
        page_url = f"{args.url}?{args.pagination}={i}"
        html = fetch_html(page_url, args.delay, not args.no_save, i)
        page_links = extract_links_from_html(html, args.link_class, base_domain)
        all_links.extend(page_links)

    unique_links = list(set(all_links))
    print(f"Total unique links found: {len(unique_links)}")

    df = pd.DataFrame({"url": unique_links})
    df.to_csv(args.output, index=False)
    print(f"Links saved to {args.output}")

if __name__ == "__main__":
    main()