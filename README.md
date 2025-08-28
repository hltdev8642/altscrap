# AltScrap Browser

A GUI browser for finding software alternatives on alternativeto.net using Scrapy for scraping.

## Features

- Enter a software name to find alternatives
- Scrapes alternativeto.net for alternatives
- Displays results in a simple GUI

## Installation

1. Install Python dependencies:
   ```bash
   pip install scrapy beautifulsoup4 requests lxml
   ```

2. Run the application:
   ```bash
   python run.py
   ```

## Project Structure

- `src/altscrap_browser/` - Main package
  - `__init__.py`
  - `main.py` - GUI application
  - `settings.py` - Scrapy settings
  - `items.py` - Scrapy item definitions
  - `pipelines.py` - Scrapy pipelines
  - `spiders/` - Scrapy spiders
    - `__init__.py`
    - `alternativeto_spider.py` - Spider for scraping alternativeto.net
- `scrapy.cfg` - Scrapy configuration
- `requirements.txt` - Python dependencies
- `run.py` - Entry point

## Usage

1. Run `python run.py`
2. Enter a software name (e.g., "firefox")
3. Click "Find Alternatives"
4. View the results in the list

## Notes

- The spider may need adjustment of CSS selectors based on the current alternativeto.net structure
- Ensure you comply with alternativeto.net's terms of service
- This is a basic implementation for demonstration
