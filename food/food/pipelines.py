# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class FoodPipeline:
    def process_item(self, item, spider):
        quantity = item.get("quantity")
        if quantity:
            # split the number and the unit
            quantity_list = quantity.split()
            # remove "," from the number
            quantity = quantity_list[0].replace(",", "")
            # assign the unit into a variable
            unit = quantity_list[1]
            # cast to number
            if "." in quantity:
                item["quantity"] = float(quantity)
            else:
                item["quantity"] = int(quantity)
            item["unit"] = unit

        return item
