[![Upload to Google Drive](https://github.com/chebishev/bb-team-info-by-ingredient/actions/workflows/xlsx_to_gdrive.yml/badge.svg)](https://github.com/chebishev/bb-team-info-by-ingredient/actions/workflows/xlsx_to_gdrive.yml)

🥦 Nutrition Scraper - bb-team.org

This project is a Scrapy-based web scraper that extracts detailed nutritional information from bb-team.org — a popular Bulgarian website for nutrition and fitness.

The scraper collects data on various food products and exports the results into a well-structured Excel file (foods.xlsx). The Excel file contains categorized nutrient information per 100 grams + almost 70 other nutrients, along with basic product details.

📋 Features

Scrapes nutrition data for a wide range of food items.

### Extracts and organizes nutrients into categories:
100 грама съдържат (Nutrients per 100 grams)

Въглехидрати (Carbohydrates)

Мазнини (Fats)

Витамини (Vitamins)

Минерали (Minerals)

Аминокиселини (Amino Acids)

Стероли (Sterols)

Още (Others)

### Also captures:

Product name + link to the product

Description

Food group + link to the food group

Outputs the data in an Excel spreadsheet (foods.xlsx)

🛠️ Technologies Used

Python 3

Scrapy – for web scraping

openpyxl – for writing Excel files

rclone - for automated uploading to Google Drive

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
        └── foods.xlsx            # the file that is uploaded automatically to Google Drive
        └── ingredients.csv       # scraped data that contains product name, description, food_group, url and nutrients
        └── ingredients.py        # main spider
        └── log_ingredients.txt   # mostly for time logging
```


📌 Notes
This project is for educational and research purposes.

Check out Read Only Version here(No filters for Viewers): [Google Drive](https://docs.google.com/spreadsheets/d/1y_o9Es5Aajau9ggKZ4CgEE1zYTVhn5Sy/edit?usp=sharing&ouid=115367196449881872914&rtpof=true&sd=true) \
or just download the latest foods.xlsx from the repo \
The data source is bb-team.org, and all rights to the content belong to them. \
You can always scrape it or modify it for yourself: \
```bash
python -m venv .venv
.\.venv\Scripts\activate
# for Linux -> source .venv\bin\activate
pip install -r requirements.txt
cd foods/foods/spiders
scrapy crawl ingredients
```

📄 License
MIT License
