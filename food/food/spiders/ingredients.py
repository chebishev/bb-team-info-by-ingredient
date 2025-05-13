import scrapy
from food.items import FoodItem
from scrapy.settings.default_settings import FEED_EXPORT_FIELDS

KEYWORD = "Калций"
FOOD_GROUPS_TO_EXCLUDE = ["Свински продукти", "Млечни и яйчни продукти"]
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
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
        "LOG_LEVEL": "WARNING",
        "LOG_FILE": f"log_{name}.txt",
        "ITEM_PIPELINES": {"food.pipelines.FoodPipeline": 300},
    }

    def parse(self, response):
        name = response.css("h1::text").get().strip()
        description = response.css("h1+p::text").get()
        for product in INGREDIENTS_TO_EXCLUDE:
            if product in name.lower() or product in description.lower():
                return
        food_group = response.css("nav>ol>li:last-child a::text").get().strip()
        if food_group in FOOD_GROUPS_TO_EXCLUDE:
            return
        url = response.url
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