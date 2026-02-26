FROM python:3.11-slim
WORKDIR /app
ENV SCRAPY_SETTINGS_MODULE=core.settings_docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY .
CMD ["scrapy", "crawl", "books", "-O", "books.json"]
