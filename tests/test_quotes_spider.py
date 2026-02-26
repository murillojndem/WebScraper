from scrapy.http import HtmlResponse
from core.spiders.quotes import QuotesSpider


def make_response(html: str, url: str = "https://quotes.toscrape.com/"):
    return HtmlResponse(url=url, body=html.encode("utf-8"), encoding="utf-8")


def test_quotes_spider_parses_items_and_next_page():
    html = """
    <html>
      <body>
        <div class="quote">
          <span class="text">“Quote One”</span>
          <small class="author">Author One</small>
          <a class="tag">life</a>
          <a class="tag">truth</a>
          <span><a href="/author/author-one">About</a></span>
        </div>
        <ul class="pager">
          <li class="next"><a href="/page/2">next</a></li>
        </ul>
      </body>
    </html>
    """
    spider = QuotesSpider()
    response = make_response(html)
    results = list(spider.parse(response))
    items = [r for r in results if isinstance(r, dict)]
    requests = [r for r in results if not isinstance(r, dict)]
    assert len(items) == 0
    assert len(requests) == 2
    author_req = requests[0]
    next_page_req = requests[1]
    assert author_req.url.endswith("/author/author-one")
    assert next_page_req.url.endswith("/page/2")


def test_quotes_spider_parse_author_enriches_quote():
    html = """
    <html>
      <body>
        <span class="author-born-date">January 1, 1900</span>
        <span class="author-born-location">in Somewhere</span>
        <div class="author-description">
          This  is   a   long   description.
        </div>
      </body>
    </html>
    """
    spider = QuotesSpider()
    response = make_response(html, url="https://quotes.toscrape.com/author/author-one")
    quote = {
        "text": "Quote One",
        "author": "Author One",
        "tags": ["truth", "life"],
    }
    result = list(spider.parse_author(response, quote))[0]
    assert result["author_born_date"] == "January 1, 1900"
    assert result["author_born_location"] == "in Somewhere"
    assert result["author_description"] == "This is a long description."
    assert result["text"] == "Quote One"
    assert result["author"] == "Author One"
    assert sorted(result["tags"]) == ["life", "truth"]
