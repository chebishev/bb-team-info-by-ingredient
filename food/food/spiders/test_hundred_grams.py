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
        "FEED_EXPORT_FIELDS": ["calories", "protein", "carbohydrates", "fats"],
        "LOG_FILE": f"log_{name}.txt"
    }

    def parse(self, response):
        if response.url == "https://www.bb-team.org/hrani":
            return

        nutritions = response.css("p.font-semibold+div > div")

        parsed = []
        for block in nutritions:
            # Try to extract the number from the span text
            number = block.css("span::text").re_first(r"[\d.,]+")
            if number:
                parsed.append(number)
            elif "Няма данни" in block.get():
                parsed.append("")  # Use empty string for missing data
        
        yield {
            "calories": parsed[0],
            "protein": parsed[1],
            "carbohydrates": parsed[2],
            "fats": parsed[3],
        }