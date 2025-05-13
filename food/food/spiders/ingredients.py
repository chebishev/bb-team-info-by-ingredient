import logging
from datetime import datetime

import scrapy
from scrapy.settings.default_settings import FEED_EXPORT_FIELDS

from food.items import FoodItem

import warnings
warnings.filterwarnings("ignore", category=scrapy.exceptions.ScrapyDeprecationWarning)

logger = logging.getLogger(__name__)

KEYWORD = "Калций"
FOOD_GROUPS_TO_EXCLUDE = ["Свински продукти", "Млечни и яйчни продукти", "Захарни изделия"]
INGREDIENTS_TO_EXCLUDE = ["пиле", "захар"]

class IngredientsSpider(scrapy.spiders.SitemapSpider):
    name = "ingredients"
    sitemap_urls = [
        "https://www.bb-team.org/sitemaps/foods",
    ]

    custom_settings = {
        # what will contain the CSV and in what order
        "FEED_EXPORT_FIELDS": ["name", "description", "food_group", "quantity", "unit", "url"],
        "FEEDS": {f"{name}.csv": {"format": "csv", "overwrite": True}},
        "LOG_LEVEL": "WARNING",
        "LOG_FILE": f"log_{name}.txt",
        "ITEM_PIPELINES": {"food.pipelines.FoodPipeline": 300},
    }

    start_time = datetime.now()

    def parse(self, response):
        name = response.css("h1::text").get().strip()
        description = response.css("h1+p::text").get()
        url = response.url
        # Escape temporary AttributeError, because of .lower() method
        if url == "https://www.bb-team.org/hrani":
            return
        for product in INGREDIENTS_TO_EXCLUDE:
            if product in name.lower() or product in description.lower():
                return
        food_group = response.css("nav>ol>li:last-child a::text").get().strip()
        if food_group in FOOD_GROUPS_TO_EXCLUDE:
            return
        
        quantity = ""
        tables = response.css("h2+table")
        keyword_found = False

        for table in tables:
            if keyword_found:
                break
            current_table = table.css("table>tbody")
            for row in current_table:
                if keyword_found:
                    break
                found_ingredients = row.css("tr")
                for ingredient in found_ingredients:
                    current_ingredient = ingredient.css("a::text").get()
                    if current_ingredient == KEYWORD:
                        quantity = ingredient.css("td::text").get()
                        keyword_found = True
                        break

        if not quantity.strip() or quantity is None:
            return

        food_item = FoodItem(
            name=name,
            description=description.strip() if description else "",
            food_group=food_group,
            quantity=quantity,
            unit="",
            url=url
        )

        yield food_item

    def closed(self, response):
        crawl_end = datetime.now()
        logger.warn(f"Crawling completed in {crawl_end - self.start_time}")
