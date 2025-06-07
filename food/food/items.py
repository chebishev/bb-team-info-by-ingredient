import scrapy

class FoodItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    food_group = scrapy.Field()
    hundred_grams_summary = scrapy.Field()
    nutrients = scrapy.Field()
    url = scrapy.Field()
