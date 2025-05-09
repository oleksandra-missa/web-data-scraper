# 🕸️ web-data-scraper

A flexible command-line tool for scraping links from paginated web listings.

This script extracts links from multiple pages based on a user-defined base URL and HTML class. It supports optional saving of raw HTML files and exports the results to a CSV file.

---

## 🚀 Features

- Scrapes links across paginated listings
- Automatically handles relative URLs by inferring domain from the base URL
- Customizable:
  - Pagination query parameter (e.g., `page`, `stranka`)
  - HTML class used for link anchors
- Optional saving of raw HTML pages
- Exports unique links to CSV

---

## 📦 Requirements

- Python 3.7+
- Install dependencies with:

```bash
pip install -r requirements.txt
```

**requirements.txt:**

```
requests
beautifulsoup4
pandas
```

---

## 🛠️ Usage

```bash
python web-data-scraper.py \
  <BASE_URL> \
  <PAGINATION_KEY> \
  <LINK_CLASS> \
  [--pages N] \
  [--delay SECONDS] \
  [--output FILE.csv] \
  [--no-save]
```

---

## 🔹 Positional Arguments

| Argument        | Description                                                                      |
|-----------------|----------------------------------------------------------------------------------|
| `BASE_URL`      | The base URL to paginate (e.g., `https://example.com/listings`)                 |
| `PAGINATION_KEY`| Name of the query parameter for pagination (e.g., `page`, `stranka`)            |
| `LINK_CLASS`    | The CSS class name used to identify `<a>` tags for link extraction              |

---

## 🔸 Optional Arguments

| Flag           | Description                                        | Default              |
|----------------|----------------------------------------------------|----------------------|
| `--pages`      | Number of pages to scrape                          | `276`                |
| `--delay`      | Delay (in seconds) between HTTP requests           | `5`                  |
| `--output`     | CSV filename to save extracted links               | `output_links.csv`   |
| `--no-save`    | If set, HTML files will **not** be saved           | Disabled (files saved by default) |

---

## 📂 Output

Generates a CSV file with unique extracted links:

```csv
url
https://example.com/item1
https://example.com/item2
...
```

If saving is enabled (default), it also creates raw HTML files like:

```
page_1.html
page_2.html
...
```

---

## 🧹 Clean-Up

To delete saved HTML pages:

```bash
rm page_*.html
```

---

## 🔧 Future Enhancements

- Extract additional data fields (e.g., titles, images)
- Add support for asynchronous scraping
- Live status display or progress bar

---

## 📄 License

MIT License