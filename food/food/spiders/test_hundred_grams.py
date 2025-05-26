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
        "FEED_EXPORT_FIELDS": ["Serving Size", "nutritions"],
        "LOG_FILE": f"log_{name}.txt"
    }

    def parse(self, response):
        if response.url == "https://www.bb-team.org/hrani":
            logger.info("Skipping the main food page.")
            return
        
        serving_size = "100 грама съдържат:"
        nutritions = response.css("p.font-semibold+div")
        nutritions_string = " ".join(n.strip() for n in nutritions.css("div span::text").getall()).replace("г", "")
        nutritions_list = " ".join(nutritions_string.split()).split()

        yield {
            "Serving Size": serving_size,
            "nutritions": f"{nutritions_list} -> {len(nutritions_list)} елемента",
        }
