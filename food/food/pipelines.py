from itemadapter import ItemAdapter
import openpyxl


class FoodPipeline:
    def process_item(self, item, spider):
        nutrients = item.get("nutrients", [])
        processed_nutrients = []

        for nutrient in nutrients:
            quantity_text = nutrient.get("raw_quantity", "")
            quantity_parts = quantity_text.split()

            if not quantity_parts:
                continue  # Skip empty or invalid

            numeric = quantity_parts[0].replace(",", "").strip()
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
                "name": f'{nutrient.get("name", "").strip()} ({unit})',
                "quantity": quantity,
                # "group": nutrient.get("group", "").strip()
            })

        item["nutrients"] = processed_nutrients
        
        return item


class XSLXPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.active

        # Predefined column headers (nutrients with units!)
        self.headers = [
            "Име", "Описание", "Хранителна група",
            "Фибри (г)", "Нишесте (г)", "Захари (г)", "Галактоза (г)", "Глюкоза (г)", "Захароза (г)", "Лактоза (г)", "Малтоза (г)", "Фруктоза (г)",
            "Бетаин (мг)", "Витамин A (IU)", "Витамин B1 (Тиамин) (мг)", "Витамин B2 (Рибофлавин) (мг)", "Витамин B3 (Ниацин) (мг)",
            "Витамин B4 (Холин) (мг)", "Витамин B5 (Пантотенова киселина) (мг)", "Витамин B6 (Пиридоксин) (мг)", "Витамин B9 (Фолиева киселина) (мкг)",
            "Витамин B12 (Кобалкамин) (мкг)", "Витамин C (мг)", "Витамин D (мкг)", "Витамин E (мг)", "Витамин K1 (мкг)", "Витамин K2 (MK04) (мкг)",
            "Аланин (г)", "Аргинин (г)", "Аспарагинова киселина (г)", "Валин (г)", "Глицин (г)", "Глутамин (г)", "Изолевцин (г)", "Левцин (г)",
            "Лизин (г)", "Метионин (г)", "Пролин (г)", "Серин (г)", "Тирозин (г)", "Треонин (г)", "Триптофан (г)", "Фенилаланин (г)", "Хидроксипролин (г)",
            "Хистидин (г)", "Цистин (г)", "Мазнини (г)", "Мононенаситени мазнини (г)", "Полиненаситени мазнини (г)", "Наситени мазнини (г)",
            "Трансмазнини (г)", "Желязо (мг)", "Калий (мг)", "Калций (мг)", "Манезий (мг)", "Манан (г)", "Мед (мг)", "Натрий (мг)", "Селен (мкг)",
            "Флуорид (мг)", "Фосфор (мг)", "Цинк (мг)", "Холестерол (мг)", "Фитостероли (мг)", "Стимастероли (мг)", "Кампестероли (мг)",
            "Бета-ситостероли (мг)", "Алкохол (г)", "Вода (г)", "Кофеин (мг)", "Теобромин (мг)", "Пепел (г)"
        ]

        self.sheet.append(self.headers)

    def process_item(self, item, spider):
        # Build a lookup dict for nutrients
        nutrient_map = {n["name"]: n["quantity"] for n in item.get("nutrients", [])}

        # Start with basic info
        row = [
            item.get("name", ""),
            item.get("description", ""),
            item.get("food_group", ""),
        ]

        # Fill each nutrient value in the correct column
        for header in self.headers[3:]:  # skip first 3
            row.append(nutrient_map.get(header, ""))

        self.sheet.append(row)
        return item

def close_spider(self, spider):
    # Freeze the first row (header row)
    self.sheet.freeze_panes = "A2"  # Everything above A2 (i.e., row 1) stays frozen

    # Auto-size all columns based on their content
    for column_cells in self.sheet.columns:
        max_length = 0
        column_letter = column_cells[0].column_letter
        for cell in column_cells:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        adjusted_width = max_length + 2  # Add a little padding
        self.sheet.column_dimensions[column_letter].width = adjusted_width

    # Save the workbook
    self.wb.save("foods.xlsx")
        