import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

for i in range(1, 277):
    print(i)
    url = f"https://www.autoesa.cz/vsechna-auta?stranka={i}"
    time.sleep(5)
    req = requests.get(url)
    html_text = req.text
    with open(f'example{i}.txt', 'w', encoding="utf-8") as file:
        file.write(html_text)
    print(req)

all_links = []
#iteracja txt
for i in range(1, 277):
    with open(f"example{i}.txt", "r", encoding="utf-8") as file:
        html_text = file.read()
        soup = BeautifulSoup(html_text, "lxml")
        links = soup.find_all("a", class_='car_item', href=True)
        for link in links:
            full_url = "https://www.autoesa.cz" + link["href"]
            all_links.append(full_url)

all_links = list(set(all_links))
print(f"Total unique links found: {len(all_links)}")

data = []