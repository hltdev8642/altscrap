import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import os

class AltScrapBrowser(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AlternativeTo.net Browser")
        self.geometry("800x600")
        self.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10))
        
        # Create main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Search Software", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Software Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.entry = ttk.Entry(input_frame, width=40)
        self.entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.entry.focus()
        
        self.search_button = ttk.Button(input_frame, text="Find Alternatives", command=self.start_scraping)
        self.search_button.grid(row=0, column=2)
        
        # Progress section
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="Ready")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        self.progress_bar.grid_remove()  # Hide initially
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Alternatives Found", padding="10")
        results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Results text area with scrollbar
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, height=15, font=('Arial', 9))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to search")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Bind Enter key to search
        self.entry.bind('<Return>', lambda e: self.start_scraping())
        
        # Threading
        self.scraping_thread = None
        self.is_scraping = False

    def start_scraping(self):
        if self.is_scraping:
            return
            
        software_name = self.entry.get().strip()
        if not software_name:
            messagebox.showwarning("Input Required", "Please enter a software name")
            self.entry.focus()
            return
        
        # Start scraping in separate thread
        self.is_scraping = True
        self.search_button.config(state='disabled', text="Searching...")
        self.progress_var.set("Searching for alternatives...")
        self.progress_bar.grid()
        self.progress_bar.start()
        self.status_var.set(f"Searching for alternatives to '{software_name}'...")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Searching...\n")
        
        self.scraping_thread = threading.Thread(target=self.scrape, args=(software_name,))
        self.scraping_thread.daemon = True
        self.scraping_thread.start()
        
        # Check thread completion
        self.after(100, self.check_scraping_status)

    def check_scraping_status(self):
        if self.scraping_thread and self.scraping_thread.is_alive():
            self.after(100, self.check_scraping_status)
        else:
            self.finish_scraping()

    def finish_scraping(self):
        self.is_scraping = False
        self.search_button.config(state='normal', text="Find Alternatives")
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
        self.progress_var.set("Search completed")
        self.status_var.set("Ready to search")

    def scrape(self, software_name):
        try:
            from selenium import webdriver
            from selenium.webdriver.firefox.options import Options
            from selenium.webdriver.firefox.service import Service
            from webdriver_manager.firefox import GeckoDriverManager
            from bs4 import BeautifulSoup
            import re

            # Update status
            self.after(0, lambda: self.progress_var.set("Initializing browser..."))
            
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            # Set Firefox binary location
            firefox_paths = [
                r"C:\Program Files\Mozilla Firefox\firefox.exe",
                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
                r"D:\PortableApps\FirefoxPortable\App\Firefox64\firefox.exe"
            ]
            
            firefox_binary = None
            for path in firefox_paths:
                if os.path.exists(path):
                    firefox_binary = path
                    break
            
            if not firefox_binary:
                raise Exception("Firefox not found. Please install Firefox or update the binary path.")

            options.binary_location = firefox_binary
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
            
            # Update status
            self.after(0, lambda: self.progress_var.set("Loading webpage..."))
            
            url = f'https://alternativeto.net/browse/search?q={software_name}'
            driver.get(url)
            
            # Update status
            self.after(0, lambda: self.progress_var.set("Parsing content..."))
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()

            # Debug: Save HTML for inspection
            with open('debug_page.html', 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            
            # Debug: Log page title and basic info
            title = soup.find('title')
            page_title = title.get_text() if title else "No title found"
            self.after(0, lambda: self.progress_var.set(f"Page loaded: {page_title}"))
            
            # Parse alternatives - updated for current alternativeto.net structure
            alternatives = []
            
            # Method 1: Look for app item containers with data-testid
            app_items = soup.find_all('li', {'data-testid': re.compile(r'^item-')})
            self.after(0, lambda: self.progress_var.set(f"Found {len(app_items)} app items"))
            
            for item in app_items:
                # Find app name in h2 tag
                name_elem = item.find('h2', class_=re.compile(r'Heading_h2'))
                if not name_elem:
                    # Fallback: look for any h2
                    name_elem = item.find('h2')
                
                if name_elem:
                    name = name_elem.get_text(strip=True)
                    
                    # Find description
                    desc_elem = item.find('p')
                    desc = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    # Find URL from the main app link
                    url_elem = item.find('a', href=re.compile(r'/software/[^/]+/about/'))
                    if not url_elem:
                        # Fallback: any software link
                        url_elem = item.find('a', href=re.compile(r'/software/'))
                    
                    url_alt = url_elem['href'] if url_elem else ""
                    
                    # Clean up the URL (remove /about/ if present)
                    if url_alt.endswith('/about/'):
                        url_alt = url_alt[:-7]  # Remove /about/
                    
                    if name and len(name) > 2 and name not in ['Alternatives', 'More about', 'Download', 'Visit', '']:
                        alternatives.append({
                            'name': name,
                            'description': desc,
                            'url': f"https://alternativeto.net{url_alt}" if url_alt.startswith('/') else url_alt
                        })

            # Method 2: If no results, try looking for app-item-container divs
            if not alternatives:
                self.after(0, lambda: self.progress_var.set("Trying alternative parsing method..."))
                
                app_containers = soup.find_all('div', class_='app-item-container')
                for container in app_containers:
                    # Find app name
                    name_elem = container.find('h2', class_=re.compile(r'Heading_h2'))
                    if not name_elem:
                        name_elem = container.find('h2')
                    
                    if name_elem:
                        name = name_elem.get_text(strip=True)
                        
                        # Find description
                        desc_elem = container.find('p')
                        desc = desc_elem.get_text(strip=True) if desc_elem else ""
                        
                        # Find URL
                        url_elem = container.find('a', href=re.compile(r'/software/'))
                        url_alt = url_elem['href'] if url_elem else ""
                        
                        if url_alt.endswith('/about/'):
                            url_alt = url_alt[:-7]
                        
                        if name and len(name) > 2:
                            alternatives.append({
                                'name': name,
                                'description': desc,
                                'url': f"https://alternativeto.net{url_alt}" if url_alt.startswith('/') else url_alt
                            })

            # Method 3: Broad search for any software links (fallback)
            if not alternatives:
                self.after(0, lambda: self.progress_var.set("Trying broad search..."))
                
                all_links = soup.find_all('a', href=re.compile(r'/software/[^/]+/?$'))
                for link in all_links[:20]:  # Limit results
                    name = link.get_text(strip=True)
                    if name and len(name) > 2 and not any(skip in name.lower() for skip in ['alternative', 'download', 'visit', 'more about']):
                        href = link['href']
                        
                        # Try to find description in nearby elements
                        desc = ""
                        parent = link.parent
                        for _ in range(3):  # Check up to 3 levels up
                            if parent:
                                desc_elem = parent.find('p')
                                if desc_elem:
                                    desc = desc_elem.get_text(strip=True)
                                    break
                                parent = parent.parent
                        
                        if href.endswith('/about/'):
                            href = href[:-7]
                            
                        alternatives.append({
                            'name': name,
                            'description': desc,
                            'url': f"https://alternativeto.net{href}" if href.startswith('/') else href
                        })
            
            # Remove duplicates
            seen_names = set()
            unique_alternatives = []
            for alt in alternatives:
                if alt['name'] not in seen_names:
                    seen_names.add(alt['name'])
                    unique_alternatives.append(alt)

            # Update results
            self.after(0, lambda: self.update_results(unique_alternatives, software_name))

        except Exception as e:
            self.after(0, lambda: self.show_error(str(e)))

    def update_results(self, alternatives, software_name):
        self.results_text.delete(1.0, tk.END)
        
        if alternatives:
            self.results_text.insert(tk.END, f"Alternatives to '{software_name}':\n\n")
            for i, alt in enumerate(alternatives[:15], 1):
                self.results_text.insert(tk.END, f"{i}. {alt['name']}\n")
                if alt['description']:
                    self.results_text.insert(tk.END, f"   {alt['description']}\n")
                if alt['url']:
                    self.results_text.insert(tk.END, f"   URL: {alt['url']}\n")
                self.results_text.insert(tk.END, "\n")
            self.progress_var.set(f"Found {len(alternatives)} alternatives")
        else:
            self.results_text.insert(tk.END, f"No alternatives found for '{software_name}'\n\nPossible reasons:\n• Website structure changed\n• Anti-bot protection\n• No alternatives available\n\nDebug file saved as 'debug_page.html' for inspection")
            self.progress_var.set("No alternatives found")

    def show_error(self, error_msg):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Error occurred:\n\n{error_msg}\n\nDebug file saved as 'debug_page.html' for inspection")
        self.progress_var.set("Error occurred")

if __name__ == "__main__":
    app = AltScrapBrowser()
    app.mainloop()
