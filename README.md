# WebScraper – Scrapy Project

A modular, containerized Scrapy project with two independent spiders, a cleaning pipeline, automated tests, multi-environment settings, and Docker support.

---

## Spiders

### `books` — [books.toscrape.com](https://books.toscrape.com)

Crawls all pages of the book catalogue, following pagination automatically.

**Extracted fields:**

| Field | Description |
|---|---|
| `title` | Book title |
| `price` | Price string (e.g. `£10.99`) |
| `price_numeric` | Parsed float price (added by pipeline) |
| `availability` | Stock status (cleaned by pipeline) |
| `url` | Absolute URL of the book page |

### `quotes` — [quotes.toscrape.com](https://quotes.toscrape.com)

Crawls all quote pages and follows each author's detail page to enrich the data.

**Extracted fields:**

| Field | Description |
|---|---|
| `text` | Quote text |
| `author` | Author name |
| `tags` | List of tags (sorted alphabetically by pipeline) |
| `author_born_date` | Author birth date |
| `author_born_location` | Author birth location |
| `author_description` | Author biography (whitespace-normalized) |

---

## Pipeline

`CleanItemPipeline` runs on all items and performs:

- **Availability**: collapses extra whitespace (e.g. `"\n    In stock\n  "` → `"In stock"`)
- **Price**: strips `£` and adds a `price_numeric` float field
- **Tags**: sorts the tag list alphabetically

---

## Project Structure

```
core/
  spiders/
    books.py           # Books spider
    quotes.py          # Quotes spider
  items.py             # Item definitions
  pipelines.py         # CleanItemPipeline
  middlewares.py       # Spider & downloader middleware stubs
  settings.py          # Entry point (imports dev settings)
  settings_base.py     # Shared settings for all environments
  settings_dev.py      # Development overrides (DEBUG log, no log file)
  settings_docker.py   # Docker overrides (INFO log, log file enabled)
tests/
  test_books_spider.py
  test_quotes_spider.py
Dockerfile
.dockerignore
requirements.txt
scrapy.cfg
```

---

## Settings Overview

| File | Used when | Log level | Log file |
|---|---|---|---|
| `settings_base.py` | Base for all | `INFO` | `scrapy.log` |
| `settings_dev.py` | Local dev | `DEBUG` | None |
| `settings_docker.py` | Docker | `INFO` | `scrapy.log` |
| `settings.py` | Default (`scrapy.cfg`) | inherits dev | None |

**Base settings highlights:**

- `DOWNLOAD_DELAY = 0.25`
- `CONCURRENT_REQUESTS_PER_DOMAIN = 1`
- `RETRY_TIMES = 3`, `DOWNLOAD_TIMEOUT = 10`
- `ROBOTSTXT_OBEY = True`
- Custom `User-Agent` header (Chrome/120)

---

## Installation (Local)

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Running Spiders (Local)

```bash
# Books spider → books.json
scrapy crawl books -O books.json

# Quotes spider → quotes.json
scrapy crawl quotes -O quotes.json
```

---

## Running Tests (Local)

```bash
pytest
```

Tests use fake `HtmlResponse` objects — no network access required.

**Coverage:**

- Field extraction for both spiders
- Pagination request generation
- Author detail page parsing (quotes spider)
- URL construction correctness

---

## Docker

The Docker image uses `python:3.11-slim` and sets `SCRAPY_SETTINGS_MODULE=core.settings_docker` automatically.

### Build

```bash
docker build -t webscraper .
```

### Run spiders

```bash
# Default command (books spider, output to books.json inside container)
docker run --rm webscraper

# Books spider with output mounted to host
docker run --rm -v "%cd%":/app webscraper scrapy crawl books -O books.json

# Quotes spider with output mounted to host
docker run --rm -v "%cd%":/app webscraper scrapy crawl quotes -O quotes.json
```

### Run tests inside container

```bash
docker run --rm -v "%cd%":/app webscraper pytest
```

---

## Technologies

- Python 3.11
- Scrapy 2.13
- pytest 9
- Docker (python:3.11-slim)
- itemadapter, lxml, parsel
