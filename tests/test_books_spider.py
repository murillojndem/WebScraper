from scrapy.http import HtmlResponse
from core.spiders.books import BooksSpider


def make_response(html: str, url: str = "https://books.toscrape.com/"):
    return HtmlResponse(url=url, body=html.encode("utf-8"), encoding="utf-8")


def test_books_spider_parses_items():
    html = """
    <html>
      <body>
        <section>
          <article class="product_pod">
            <h3><a href="book1.html" title="Book One"></a></h3>
            <p class="price_color">£10.00</p>
            <p class="availability">
                In stock
            </p>
          </article>

          <article class="product_pod">
            <h3><a href="book2.html" title="Book Two"></a></h3>
            <p class="price_color">£20.00</p>
            <p class="availability">
                5 in stock
            </p>
          </article>
        </section>
        <ul class="pager">
          <li class="next"><a href="page-2.html">next</a></li>
        </ul>
      </body>
    </html>
    """

    spider = BooksSpider()
    response = make_response(html)

    results = list(spider.parse(response))

    # devem existir 2 itens + 1 request de próxima página
    items = [r for r in results if isinstance(r, dict)]
    requests = [r for r in results if not isinstance(r, dict)]

    assert len(items) == 2

    assert items[0]["title"] == "Book One"
    assert items[0]["price"] == "£10.00"
    assert items[0]["availability"] == "In stock"
    assert items[0]["url"].endswith("book1.html")

    assert items[1]["title"] == "Book Two"
    assert items[1]["price"] == "£20.00"
    assert items[1]["availability"] == "5 in stock"
    assert items[1]["url"].endswith("book2.html")

    # verifica se criou um request para a próxima página
    assert len(requests) == 1
    assert requests[0].url.endswith("page-2.html")
