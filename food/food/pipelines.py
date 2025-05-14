from itemadapter import ItemAdapter

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
                "name": nutrient.get("name", "").strip(),
                "quantity": quantity,
                "unit": unit,
                "group": nutrient.get("group", "").strip()
            })

        item["nutrients"] = processed_nutrients
        return item
