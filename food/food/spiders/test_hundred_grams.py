from scrapy.spiders import SitemapSpider
import logging

logger = logging.getLogger(__name__)

class HundredGramsSpider(SitemapSpider):
    name = "hundred_grams"
    sitemap_urls = [
        "https://www.bb-team.org/sitemaps/foods",
    ]

    custom_settings = {
        "LOG_LEVEL": "WARNING",
        "FEEDS": {
            f"{name}.csv": {"format": "csv", "overwrite": True}
        },
        "FEED_EXPORT_FIELDS": ["Serving Size", "calories", "proteine", "carbonates", "fats"],
        "LOG_FILE": f"log_{name}.txt"
    }

    def _parse(self, response):
        serving_size_list = response.css("p.font-semibold ::text").getall()
        serving_size = " ".join(text.strip() for text in serving_size_list).strip()

        yield {
            "Serving Size": serving_size_list[0] if serving_size_list else None,
            "calories": response.css("p.text-2xl::text").get(),
            "proteine": response.css("p.text-2xl+ p::text").get(),
            "carbonates": response.css("p.text-2xl+ p+ p::text").get(),
            "fats": response.css("p.text-2xl+ p+ p+ p::text").get(),
        }