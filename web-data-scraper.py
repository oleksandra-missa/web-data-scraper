import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import os

def download_html_pages(base_url: str, pagination_key: str, num_pages: int, delay: int = 5):
    for i in range(1, num_pages + 1):
        print(f"Downloading page {i}")
        params = {pagination_key: i}
        response = requests.get(base_url, params=params)
        html_text = response.text
        with open(f'page_{i}.html', 'w', encoding="utf-8") as file:
            file.write(html_text)
        print(f"Saved: page_{i}.html (Status: {response.status_code})")
        time.sleep(delay)

def extract_links_from_files(num_pages: int, link_class: str, domain: str) -> list:
    all_links = []
    for i in range(1, num_pages + 1):
        file_name = f"page_{i}.html"
        if not os.path.exists(file_name):
            print(f"File {file_name} not found, skipping.")
            continue
        with open(file_name, "r", encoding="utf-8") as file:
            html_text = file.read()
            soup = BeautifulSoup(html_text, "lxml")
            links = soup.find_all("a", class_=link_class, href=True)
            for link in links:
                href = link["href"]
                full_url = href if href.startswith("http") else domain.rstrip("/") + href
                all_links.append(full_url)
    all_links = list(set(all_links))  # remove duplicates
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
    args = parser.parse_args()

    print("Starting HTML download...")
    download_html_pages(args.url, args.pagination, args.pages, args.delay)

    print("Extracting links...")
    links = extract_links_from_files(args.pages, args.link_class, args.domain)
    print(f"Total unique links found: {len(links)}")

    save_links_to_csv(links, args.output)

if __name__ == "__main__":
    main()