# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FoodItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    description = scrapy.Field()
    food_group = scrapy.Field()
    quantity = scrapy.Field()
    unit = scrapy.Field()
    url = scrapy.Field()
