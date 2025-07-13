import openpyxl
from openpyxl.styles import Alignment


class FoodPipeline:
    def process_item(self, item, spider):
        nutrients = item.get("nutrients", [])
        print(nutrients)
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
            processed_nutrients.append(
                {
                    "name": f'{nutrient.get("name", "").strip()} ({unit})',
                    "quantity": quantity,
                    # "group": nutrient.get("group", "").strip()
                }
            )
        print("*" * 50)
        print(processed_nutrients)
        item["nutrients"] = processed_nutrients

        return item


class XSLXPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.active

        self.headers = [
            "Име",
            "Описание",
            "Хранителна група",
            "Калории",
            "Протеини (г)",
            "Въглехидрати (г)",
            "Мазнини (г)",
            "Фибри (г)",
            "Нишесте (г)",
            "Захари (г)",
            "Галактоза (г)",
            "Глюкоза (г)",
            "Захароза (г)",
            "Лактоза (г)",
            "Малтоза (г)",
            "Фруктоза (г)",
            "Бетаин (мг)",
            "Витамин A (IU)",
            "Витамин B1 (Тиамин) (мг)",
            "Витамин B2 (Рибофлавин) (мг)",
            "Витамин B3 (Ниацин) (мг)",
            "Витамин B4 (Холин) (мг)",
            "Витамин B5 (Пантотенова киселина) (мг)",
            "Витамин B6 (Пиридоксин) (мг)",
            "Витамин B9 (Фолиева киселина) (мкг)",
            "Витамин B12 (Кобалкамин) (мкг)",
            "Витамин C (мг)",
            "Витамин D (мкг)",
            "Витамин E (мг)",
            "Витамин K1 (мкг)",
            "Витамин K2 (MK04) (мкг)",
            "Аланин (г)",
            "Аргинин (г)",
            "Аспарагинова киселина (г)",
            "Валин (г)",
            "Глицин (г)",
            "Глутамин (г)",
            "Изолевцин (г)",
            "Левцин (г)",
            "Лизин (г)",
            "Метионин (г)",
            "Пролин (г)",
            "Серин (г)",
            "Тирозин (г)",
            "Треонин (г)",
            "Триптофан (г)",
            "Фенилаланин (г)",
            "Хидроксипролин (г)",
            "Хистидин (г)",
            "Цистин (г)",
            "Мазнини (г)",
            "Мононенаситени мазнини (г)",
            "Полиненаситени мазнини (г)",
            "Наситени мазнини (г)",
            "Трансмазнини (г)",
            "Желязо (мг)",
            "Калий (мг)",
            "Калций (мг)",
            "Манезий (мг)",
            "Манан (г)",
            "Мед (мг)",
            "Натрий (мг)",
            "Селен (мкг)",
            "Флуорид (мг)",
            "Фосфор (мг)",
            "Цинк (мг)",
            "Холестерол (мг)",
            "Фитостероли (мг)",
            "Стимастероли (мг)",
            "Кампестероли (мг)",
            "Бета-ситостероли (мг)",
            "Алкохол (г)",
            "Вода (г)",
            "Кофеин (мг)",
            "Теобромин (мг)",
            "Пепел (г)",
        ]

        # Insert an empty row for category headers
        self.sheet.append([""] * len(self.headers))
        self.sheet.append(self.headers)

        # Define column category groupings (1-based index)
        category_ranges = {
            "100 грама съдържат": (4, 7),
            "Въглехидрати": (8, 16),
            "Витамини": (17, 31),
            "Аминокиселини": (32, 50),
            "Мазнини": (51, 55),
            "Минерали": (56, 66),
            "Стероли": (67, 71),
            "Други": (72, 76),
        }

        # Merge cells and assign group names
        for category, (start, end) in category_ranges.items():
            self.sheet.merge_cells(
                start_row=1, start_column=start, end_row=1, end_column=end
            )
            cell = self.sheet.cell(row=1, column=start)
            cell.value = category
            cell.alignment = Alignment(horizontal="center", vertical="center")

    def process_item(self, item, spider):
        nutrient_map = {n["name"]: n["quantity"] for n in item.get("nutrients", [])}
        row = [
            item.get("name", ""),
            item.get("description", ""),
            item.get("food_group", ""),
        ]
        for header in self.headers[3:]:
            row.append(nutrient_map.get(header, ""))
        self.sheet.append(row)
        return item

    def close_spider(self, spider):
        self.sheet.freeze_panes = "A3"

        for column_cells in self.sheet.columns:
            # Skip merged cells and find a real cell to get the column letter
            for cell in column_cells:
                if not isinstance(cell, openpyxl.cell.cell.MergedCell):
                    column_letter = cell.column_letter
                    break
            else:
                continue  # all cells in this column are merged, skip

            max_length = max(
                (len(str(cell.value)) for cell in column_cells if cell.value),
                default=0
            )
            self.sheet.column_dimensions[column_letter].width = max_length + 2

        self.wb.save("foods.xlsx")