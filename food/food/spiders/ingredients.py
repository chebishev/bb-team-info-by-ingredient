import logging
from datetime import datetime

from food.items import FoodItem
from scrapy.spiders import SitemapSpider

logger = logging.getLogger(__name__)


class IngredientsSpider(SitemapSpider):
    name = "ingredients"
    sitemap_urls = [
        "https://www.bb-team.org/sitemaps/foods",
    ]

    custom_settings = {
        "ITEM_PIPELINES": {
            "food.pipelines.FoodPipeline": 100,
            "food.pipelines.XSLXPipeline": 200,
        },
        "LOG_LEVEL": "WARNING",
        "FEEDS": {f"{name}.csv": {"format": "csv", "overwrite": True}},
        "FEED_EXPORT_FIELDS": ["name", "description", "food_group", "url", "nutrients"],
        "LOG_FILE": f"log_{name}.txt",
    }

    start_time = datetime.now()

    def parse(self, response):
        url = response.url
        if url == "https://www.bb-team.org/hrani":
            return

        name = response.css("h1::text").get().strip()
        description = response.css("h1+p::text").get().strip()
        food_group = response.css("nav > ol > li:last-child a")
        food_group_name = food_group.css("::text").get().strip()
        food_group_url = food_group.css("a").attrib.get("href")
        nutritions_per_100_grams = response.css("p.font-semibold+div > div")
        serving_size = "100 г съдържат:"
        hundred_grams_nutrients = ("Калории", "Протеин", "Въглехидрати", "Мазнини")
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

        nutrients = []
        for index, nutrition in enumerate(parsed_nutritions):
            nutrients.append(
                {
                    "group": serving_size,
                    "name": hundred_grams_nutrients[index],
                    "raw_quantity": (
                        f"{nutrition} к" if index == 0 else f"{nutrition} г"
                    ),
                }
            )

        for table in tables:
            summary = table.attrib.get("summary", "").strip()
            for row in table.css("tr"):
                nutrient_name = row.css("a::text").get()
                quantity_text = row.css("td::text").get()

                if not nutrient_name or not quantity_text:
                    continue

                if "няма данни" in quantity_text.lower():
                    continue

                nutrients.append(
                    {
                        "group": summary,  # Optional: use this if you want to group
                        "name": nutrient_name.strip(),
                        "raw_quantity": quantity_text.strip(),
                    }
                )
        food_item = FoodItem(
            name=name,
            description=description,
            food_group=food_group_name,
            nutrients=nutrients,
            url=url,
            food_group_url=food_group_url,
        )

        yield food_item

    def closed(self, reason):
        crawl_end = datetime.now()
        logger.warning(f"Crawling completed in {crawl_end - self.start_time}")
