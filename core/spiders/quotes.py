import scrapy
from scrapy.http import Response


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response: Response):
        for quote in response.css("div.quote"):
            author_url = quote.css("span a::attr(href)").get()
            base_data = {
                "text": quote.css("span.text::text").get().strip("“”"),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("a.tag::text").getall(),
            }
            if author_url:
                yield response.follow(
                    author_url,
                    callback=self.parse_author,
                    cb_kwargs={"quote": base_data},
                )
            else:
                yield base_data
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response: Response, quote: dict):
        quote["author_born_date"] = response.css(
            "span.author-born-date::text"
        ).get()
        quote["author_born_location"] = response.css(
            "span.author-born-location::text"
        ).get()
        description = response.css("div.author-description::text").get(default="")
        quote["author_description"] = " ".join(description.split())
        yield quote
