import logging
from datetime import datetime

import scrapy
from scrapy.spiders import SitemapSpider

from food.items import FoodItem
from food.utils import ingredients

logger = logging.getLogger(__name__)

class IngredientsSpider(SitemapSpider):
    name = "ingredients"
    sitemap_urls = [
        "https://www.bb-team.org/sitemaps/foods",
    ]

    custom_settings = {
        "ITEM_PIPELINES": 
        {"food.pipelines.FoodPipeline": 100,
        "food.pipelines.XSLXPipeline": 200},
        "LOG_LEVEL": "WARNING",
        "FEEDS": {
            f"{name}.csv": {"format": "csv", "overwrite": True}
        },
        "FEED_EXPORT_FIELDS": ["name", "description", "food_group", "nutrients", "url"],
        "LOG_FILE": f"log_{name}.txt"
    }

    start_time = datetime.now()

    def parse(self, response):
        url = response.url
        if url == "https://www.bb-team.org/hrani":
            return

        name = response.css("h1::text").get().strip()
        description = response.css("h1+p::text").get().strip()     
        food_group = response.css("nav > ol > li:last-child a::text").get().strip()

        tables = response.css("h2+table")
        if not tables:
            return

        nutrients = []

        for table in tables:
            # summary = table.attrib.get("summary", "").strip()
            for row in table.css("tr"):
                nutrient_name = row.css("a::text").get()
                quantity_text = row.css("td::text").get()

                if not nutrient_name or not quantity_text:
                    continue

                if "няма данни" in quantity_text.lower():
                    continue

                nutrients.append({
                    # "group": summary,  # Optional: use this if you want to group
                    "name": nutrient_name.strip(),
                    "raw_quantity": quantity_text.strip()
                })

        food_item = FoodItem(
            name=name,
            description=description,
            food_group=food_group.strip(),
            nutrients=nutrients,  # now a list of dicts
            url=url,
        )

        yield food_item

    def closed(self, reason):
        crawl_end = datetime.now()
        logger.warning(f"Crawling completed in {crawl_end - self.start_time}")
