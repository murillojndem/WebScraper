# WebScraper – Scrapy Project

This project is a fully containerized Scrapy implementation created as part of a technical assessment.  
It contains two independent spiders, automated tests, a cleaning pipeline, antiban configuration, separated settings for different environments, and Docker support following industry best practices.

---

## Features

- Clean and modular Scrapy project layout
- Multiple spiders (`books` and `quotes`)
- Full pagination handling
- Structured item extraction
- Cleaning pipeline with normalization and numeric conversion
- Automated tests using pytest
- Separated settings: base, development, and Docker
- Docker image for running spiders or tests
- JSON output via Scrapy’s feed exporter
- Basic antiban configuration (user-agent, retries, timeouts, delay)
- Logging configuration with file output in Docker

---

## Installation (Local Environment)

### 1. Create and activate a virtual environment

```python -m venv .venv```
```.\.venv\Scripts\activate```

### 2. Install dependencies

```pip install -r requirements.txt```

---

## Running the Spiders (Locally)

Local runs use the development settings module by default.

### Books spider

```scrapy crawl books -O books.json```

### Quotes spider

```scrapy crawl quotes -O quotes.json```

---

## Running Tests (Local)

pytest

Tests cover:

- Parsing logic for both spiders
- Pagination handling
- Field extraction
- URL correctness
- Pipeline behavior (if tests are added)

---

## Docker Support

Docker runs use the Docker settings module automatically through `SCRAPY_SETTINGS_MODULE`.

### 1. Build the Docker image

```docker build -t webscraper .```

### 2. Run the books spider inside Docker

```docker run --rm webscraper scrapy crawl books -O books.json```

### 3. Run the quotes spider inside Docker

```docker run --rm webscraper scrapy crawl quotes -O quotes.json```

### 4. Save output to your machine (bind mount)

```docker run --rm -v "%cd%":/app webscraper scrapy crawl books -O books.json```
```docker run --rm -v "%cd%":/app webscraper scrapy crawl quotes -O quotes.json```

### 5. Run the test suite inside Docker

```docker run --rm -v "%cd%":/app webscraper pytest```

---

## Settings Structure

The project uses multiple settings modules:

core/settings_base.py  
- Shared configuration for all environments

core/settings_dev.py  
- Local development settings (debug logging, no log file)

core/settings_docker.py  
- Production-like settings for container execution (log file enabled)

core/settings.py  
- Alias that imports development settings

scrapy.cfg  
- Uses `core.settings_dev` by default

Dockerfile  
- Sets `SCRAPY_SETTINGS_MODULE=core.settings_docker`

---

## Project Structure

core/
  spiders/
    books.py
    quotes.py
  items.py
  pipelines.py
  middlewares.py
  settings.py
  settings_base.py
  settings_dev.py
  settings_docker.py
tests/
  test_books_spider.py
  test_quotes_spider.py
Dockerfile
.dockerignore
requirements.txt
scrapy.cfg

---

## Technologies Used

- Python 3.11
- Scrapy 2.13
- Pytest 9
- Docker (Python 3.11-slim base image)
