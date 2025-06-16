# Web Scraping & Data Extraction for Contract Data

## Overview
This project demonstrates a web scraping solution that extracts detailed contract data from a structured HTML table on a government procurement website. The scraper collects key fields such as publication date, contract types, descriptions, contract values, deadlines, and more.

The extracted data is organized and saved in a CSV file with consistent column headers suitable for import into SQL databases or further data analysis.

## Features
- Uses Selenium WebDriver for robust scraping of dynamic web content
- Navigates HTML tables using CSS selectors, currently focused on the first search result link (functionality is a work in progress and can be extended)
- Creates SQL CREATE TABLE statements based on scraped column names and data types
- Outputs structured CSV files ready for database import or reporting

## How to Use
1. Install dependencies (see requirements.txt)
2. Update the script with your target CPV number
3. Run the scraper:
   ```bash
   python main.py
