[![Upload to Google Drive](https://github.com/chebishev/bb-team-info-by-ingredient/actions/workflows/xlsx_to_gdrive.yml/badge.svg)](https://github.com/chebishev/bb-team-info-by-ingredient/actions/workflows/xlsx_to_gdrive.yml)

🥦 Nutrition Scraper - bb-team.org
This project is a Scrapy-based web scraper that extracts detailed nutritional information from bb-team.org — a popular Bulgarian website for nutrition and fitness.

The scraper collects data on various food products and exports the results into a well-structured Excel file (foods.xlsx). The Excel file contains categorized nutrient information per 100 grams + almost 70 other nutrients, along with basic product details.

📋 Features
Scrapes nutrition data for a wide range of food items.

Extracts and organizes nutrients into categories:
100 грама съдържат

Въглехидрати (Carbohydrates)

Мазнини (Fats)

Витамини (Vitamins)

Минерали (Minerals)

Аминокиселини (Amino Acids)

Стероли (Sterols)

Още (Others)

Also captures:

Product name + link to the product

Description

Food group + link to the food group

Outputs the data in an Excel spreadsheet (foods.xlsx)

🛠️ Technologies Used
Python 3

Scrapy – for web scraping

openpyxl – for writing Excel files

📂 Project Structure
```bash
nutrition_scraper/
├── scrapy.cfg
└── foods/
   ├── __init__.py
   ├── items.py
   ├── pipelines.py
   ├── settings.py
   └── spiders/       
        └── ingredients.py
        └── foods.xlsx
```


📌 Notes
This project is for educational and research purposes.

The data source is bb-team.org, and all rights to the content belong to them.

📄 License
MIT License
