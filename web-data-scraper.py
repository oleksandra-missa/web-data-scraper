import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import os

def download_html_pages(base_url: str, num_pages: int, delay: int = 5):
    for i in range(1, num_pages + 1):
        print(f"Downloading page {i}")
        url = f"{base_url}?stranka={i}"
        time.sleep(delay)
        response = requests.get(url)
        html_text = response.text
        with open(f'example{i}.txt', 'w', encoding="utf-8") as file:
            file.write(html_text)
        print(f"Saved: example{i}.txt (Status: {response.status_code})")

def extract_links_from_files(num_pages: int) -> list:
    all_links = []
    for i in range(1, num_pages + 1):
        file_name = f"example{i}.txt"
        if not os.path.exists(file_name):
            print(f"File {file_name} not found, skipping.")
            continue
        with open(file_name, "r", encoding="utf-8") as file:
            html_text = file.read()
            soup = BeautifulSoup(html_text, "lxml")
            links = soup.find_all("a", class_='car_item', href=True)
            for link in links:
                full_url = "https://www.autoesa.cz" + link["href"]
                all_links.append(full_url)
    all_links = list(set(all_links))  # remove duplicates
    return all_links

def save_links_to_csv(links: list, filename: str = "car_links.csv"):
    df = pd.DataFrame(links, columns=["url"])
    df.to_csv(filename, index=False)
    print(f"Saved {len(links)} unique links to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Scrape car listings from autoesa.cz")
    parser.add_argument("url", type=str, help="Base URL of the listing pages (e.g., https://www.autoesa.cz/vsechna-auta)")
    parser.add_argument("--pages", type=int, default=276, help="Number of pages to scrape (default: 276)")
    parser.add_argument("--delay", type=int, default=5, help="Delay between requests in seconds (default: 5)")
    args = parser.parse_args()

    print("Starting download...")
    download_html_pages(args.url, args.pages, args.delay)
    print("Extracting links...")
    links = extract_links_from_files(args.pages)
    print(f"Total unique links found: {len(links)}")
    save_links_to_csv(links)

if __name__ == "__main__":
    main()