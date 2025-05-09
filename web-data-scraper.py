import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import os

def extract_links_from_html(html_text: str, link_class: str, domain: str) -> list:
    soup = BeautifulSoup(html_text, "lxml")
    links = soup.find_all("a", class_=link_class, href=True)
    extracted = []
    for link in links:
        href = link["href"]
        full_url = href if href.startswith("http") else domain.rstrip("/") + href
        extracted.append(full_url)
    return extracted

def scrape_pages(base_url: str, pagination_key: str, num_pages: int, delay: int, 
                 link_class: str, domain: str, save_html: bool) -> list:
    all_links = []
    for i in range(1, num_pages + 1):
        print(f"Processing page {i}")
        params = {pagination_key: i}
        response = requests.get(base_url, params=params)
        html_text = response.text

        if save_html:
            with open(f'page_{i}.html', 'w', encoding="utf-8") as file:
                file.write(html_text)
            print(f"Saved: page_{i}.html (Status: {response.status_code})")

        links = extract_links_from_html(html_text, link_class, domain)
        all_links.extend(links)

        time.sleep(delay)

    all_links = list(set(all_links))  # Remove duplicates
    return all_links

def save_links_to_csv(links: list, filename: str):
    df = pd.DataFrame(links, columns=["url"])
    df.to_csv(filename, index=False)
    print(f"Saved {len(links)} unique links to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Scrape listing links from paginated HTML pages.")
    parser.add_argument("url", type=str, help="Base URL without pagination (e.g., https://example.com/listings)")
    parser.add_argument("pagination", type=str, help="Pagination query key (e.g., page, stranka)")
    parser.add_argument("domain", type=str, help="Domain to prepend to relative links (e.g., https://example.com)")
    parser.add_argument("link_class", type=str, help="Class name of anchor tags to extract (e.g., car_item)")
    parser.add_argument("--pages", type=int, default=276, help="Number of pages to scrape (default: 276)")
    parser.add_argument("--delay", type=int, default=5, help="Delay between requests (default: 5s)")
    parser.add_argument("--output", type=str, default="output_links.csv", help="Output CSV file name")
    parser.add_argument("--no-save", action="store_true", help="Do not save HTML files locally")
    args = parser.parse_args()

    print("Starting scraping...")
    links = scrape_pages(
        base_url=args.url,
        pagination_key=args.pagination,
        num_pages=args.pages,
        delay=args.delay,
        link_class=args.link_class,
        domain=args.domain,
        save_html=not args.no_save
    )

    print(f"Total unique links found: {len(links)}")
    save_links_to_csv(links, args.output)

if __name__ == "__main__":
    main()