from itemadapter import ItemAdapter
import openpyxl
from .nutrient_headers import NUTRIENT_HEADERS

class FoodPipeline:
    def process_item(self, item, spider):
        nutrients = item.get("nutrients", [])
        processed_nutrients = []

        for nutrient in nutrients:
            quantity_text = nutrient.get("raw_quantity", "")
            quantity_parts = quantity_text.split()

            if not quantity_parts:
                continue  # Skip empty or invalid

            numeric = quantity_parts[0].replace(",", ".").strip()
            if len(quantity_parts) > 1:
                unit = quantity_parts[1]  
            else:
                continue

            # Convert to float or int
            try:
                quantity = float(numeric) if "." in numeric else int(numeric)
            except ValueError:
                quantity = None
                spider.logger.warning(
                    f"Failed to convert quantity: {numeric} in {item['url']} ({nutrient.get('name')})"
                )

            # Store cleaned nutrient info
            processed_nutrients.append({
                "name": f'{nutrient.get("name", "").strip()} {unit}',
                "quantity": quantity,
                # "group": nutrient.get("group", "").strip()
            })

        item["nutrients"] = processed_nutrients
        
        return item


class XSLXPipeline:
    def open_spider(self, spider):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = "Храни"

        # Create the header
        self.headers = ["Име", "Описание", "Хранителна група"] + list(NUTRIENT_HEADERS.values())
        self.ws.append(self.headers)

    def process_item(self, item, spider):
        nutrient_map = {nutrient["name"]: nutrient["quantity"] for nutrient in item.get("nutrients", [])}

        row = [
            item.get("name", ""),
            item.get("description", ""),
            item.get("food_group", "")
        ]

        # Append each nutrient in order of headers
        for name in NUTRIENT_HEADERS:
            row.append(nutrient_map.get(name))  # May be None

        self.ws.append(row)
        return item

    def close_spider(self, spider):
        self.wb.save("output.xlsx")