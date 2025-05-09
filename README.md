# 🕸️ web-data-scraper

A flexible command-line tool for scraping links from paginated web listings.

This tool extracts links from multiple pages based on user-defined URL structure, HTML class names, and other parameters. You can save the HTML files locally for inspection or scrape directly from memory.

---

## 🚀 Features

- Scrapes links across paginated listings
- Customizable:
  - Pagination query parameter (e.g., `page`, `stranka`)
  - HTML class used for link anchors
  - Domain for relative URLs
- Option to save raw HTML pages or skip them
- Exports results to CSV

---

## 📦 Requirements

- Python 3.7+
- Dependencies:
  - `requests`
  - `beautifulsoup4`
  - `pandas`

Install using:

```bash
pip install -r requirements.txt
```

Sample `requirements.txt`:

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
  <DOMAIN> \
  <LINK_CLASS> \
  [--pages N] \
  [--delay SECONDS] \
  [--output FILE.csv] \
  [--no-save]
```

---

## 🔹 Positional Arguments

| Argument        | Description                                                                    |
|-----------------|--------------------------------------------------------------------------------|
| `BASE_URL`      | The base URL to paginate (e.g., `https://example.com/listings`)               |
| `PAGINATION_KEY`| Name of the query parameter for pagination (e.g., `page`, `stranka`)          |
| `DOMAIN`        | The base domain to prepend to relative links (e.g., `https://example.com`)    |
| `LINK_CLASS`    | The CSS class name used to identify `<a>` tags for extraction                 |

---

## 🔸 Optional Arguments

| Flag             | Description                                     | Default              |
|------------------|-------------------------------------------------|----------------------|
| `--pages`        | Number of paginated pages to scrape             | `276`                |
| `--delay`        | Delay between HTTP requests in seconds          | `5`                  |
| `--output`       | CSV filename to save the extracted links        | `output_links.csv`   |
| `--no-save`      | If set, HTML files will **not** be saved        | disabled (files saved by default) |

---

## 📂 Output

The script generates a CSV file with all unique links found:

```csv
url
https://example.com/item1
https://example.com/item2
...
```

If HTML saving is enabled (default), it also creates local files like:

```
page_1.html
page_2.html
...
```

---

## 🧹 Clean-Up

To remove saved HTML files (if generated), run:

```bash
rm page_*.html
```

---

## 🔧 Future Enhancements

- Extract more data fields (title, price, metadata)
- Add progress bar or live status
- Enable parallel or asynchronous scraping
- Support for nested pagination

---

## 📄 License

MIT License