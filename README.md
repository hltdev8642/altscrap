# 🔍 AltScrap Browser

A modern GUI browser for finding software alternatives on alternativeto.net using Selenium for web scraping and CustomTkinter for a beautiful, modern interface.

## ✨ Features

- **Modern UI**: Beautiful CustomTkinter interface with dark/light mode support
- **Smart Search**: Enter any software name to find alternatives
- **Real-time Scraping**: Uses Selenium to scrape alternativeto.net for up-to-date results
- **Responsive Design**: Threaded scraping prevents UI freezing during searches
- **Export Functionality**: Save results to text or CSV files
- **Progress Tracking**: Visual progress indicators and status updates
- **Error Handling**: Robust error handling with debug file generation

## 🚀 Installation

1. **Clone the repository** (if not already done):

   ```bash
   git clone https://github.com/TomSchimansky/CustomTkinter.git
   ```

2. **Install dependencies**:

   ```bash
   pip install -e CustomTkinter/
   pip install selenium webdriver-manager beautifulsoup4 requests lxml
   ```

3. **Install Firefox** (required for web scraping):
   - Download from: [https://www.mozilla.org/firefox/](https://www.mozilla.org/firefox/)
   - Or update the Firefox binary path in `main.py` if using a custom location

## 🎯 Usage

1. **Run the application**:

   ```bash
   cd src/altscrap_browser
   python main.py
   ```

2. **Search for alternatives**:
   - Enter a software name (e.g., "firefox", "chrome", "vscode")
   - Click "🔍 Find Alternatives" or press Enter
   - Wait for the scraping to complete

3. **View results**:
   - Results appear in the text area below
   - Each alternative includes name, description, and URL
   - Export results using the "💾 Export Results" button

## 🏗️ Project Structure

```text
altscrap/
├── src/altscrap_browser/          # Main application package
│   ├── main.py                    # Modern CustomTkinter GUI
│   ├── settings.py               # Scrapy settings
│   ├── items.py                  # Scrapy item definitions
│   ├── pipelines.py              # Scrapy pipelines
│   └── spiders/                  # Scrapy spiders
├── CustomTkinter/                # CustomTkinter library (cloned)
├── requirements.txt              # Python dependencies
├── debug_page.html              # Debug output (generated)
├── output.json                  # Scrapy output (generated)
└── README.md                    # This file
```

## 🎨 UI Features

- **Dark/Light Mode**: Automatically adapts to system theme
- **Modern Design**: Material Design-inspired interface
- **Responsive Layout**: Adapts to different window sizes
- **Visual Feedback**: Progress bars, status indicators, and emojis
- **Intuitive Controls**: Clear buttons and input fields

## 🔧 Technical Details

- **GUI Framework**: CustomTkinter (modern Tkinter wrapper)
- **Web Scraping**: Selenium WebDriver with Firefox
- **Browser Management**: WebDriver Manager for automatic driver updates
- **HTML Parsing**: BeautifulSoup4 for content extraction
- **Threading**: Python threading for responsive UI
- **Error Handling**: Comprehensive exception handling with debug output

## 🐛 Troubleshooting

### Common Issues

1. **Firefox not found**:
   - Install Firefox browser
   - Update the `firefox_paths` list in `main.py` with your Firefox installation path

2. **No alternatives found**:
   - Check `debug_page.html` for the actual page content
   - AlternativeTo.net may have changed their website structure
   - Anti-bot protection may be active

3. **Import errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Install CustomTkinter: `pip install -e CustomTkinter/`

### Debug Files

- `debug_page.html`: Saved HTML content for inspection
- `output.json`: Scrapy output (if using Scrapy instead of Selenium)

## 📝 Notes

- The application uses Selenium for reliable scraping of dynamic content
- CustomTkinter provides a modern, customizable appearance
- Threading ensures the UI remains responsive during scraping operations
- Debug files are automatically generated for troubleshooting
- Ensure compliance with alternativeto.net's terms of service

## 🔄 Future Enhancements

- [ ] Add more export formats (JSON, XML)
- [ ] Implement search history
- [ ] Add favorite alternatives feature
- [ ] Support for multiple search engines
- [ ] Batch processing capabilities
