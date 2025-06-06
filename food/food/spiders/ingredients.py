import logging
from datetime import datetime

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
        "FEED_EXPORT_FIELDS": ["name", "description", "food_group", "hundred_grams_summary", "nutrients", "url"],
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
        nutritions_per_100_grams = response.css("p.font-semibold+div > div")
        serving_size = "100 г съдържат:"
        parsed_nutritions = []
        for block in nutritions_per_100_grams:
            number = block.css("span::text").re_first(r"[\d.,]+")
            if number:
                parsed_nutritions.append(number)
            elif "Няма данни" in block.get():
                parsed_nutritions.append("")

        tables = response.css("h2+table")
        if not tables:
            return

        hundred_grams_summary = [{
            "group": serving_size,
            "calories": parsed_nutritions[0],
            "protein": parsed_nutritions[1],
            "carbohydrates": parsed_nutritions[2],
            "fats": parsed_nutritions[3]
            }]

        nutrients = []
        for table in tables:
            summary = table.attrib.get("summary", "").strip()
            for row in table.css("tr"):
                nutrient_name = row.css("a::text").get()
                quantity_text = row.css("td::text").get()

                if not nutrient_name or not quantity_text:
                    continue

                if "няма данни" in quantity_text.lower():
                    continue

                nutrients.append({
                    "group": summary,  # Optional: use this if you want to group
                    "name": nutrient_name.strip(),
                    "raw_quantity": quantity_text.strip()
                })

        food_item = FoodItem(
            name=name,
            description=description,
            food_group=food_group.strip(),
            hundred_grams_summary=hundred_grams_summary,
            nutrients=nutrients,
            url=url,
        )

        yield food_item

    def closed(self, reason):
        crawl_end = datetime.now()
        logger.warning(f"Crawling completed in {crawl_end - self.start_time}")
