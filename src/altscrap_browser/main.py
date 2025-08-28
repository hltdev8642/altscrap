import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import threading
import os
import re

# Set CustomTkinter appearance
ctk.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class AltScrapBrowser(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔍 AlternativeTo.net Browser")
        self.geometry("1200x700")
        self.resizable(True, True)
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Header section (spans both columns)
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(header_frame, text="🔍 AlternativeTo.net Browser", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        subtitle_label = ctk.CTkLabel(header_frame, text="Find alternative software solutions", 
                                     font=ctk.CTkFont(size=12), text_color="gray")
        subtitle_label.grid(row=1, column=0)
        
        # Input section (spans both columns)
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        input_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(input_frame, text="Software Name:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, sticky="w", padx=(20, 15), pady=20)
        
        self.entry = ctk.CTkEntry(input_frame, width=400, height=40, font=ctk.CTkFont(size=12))
        self.entry.grid(row=0, column=1, sticky="ew", padx=(0, 15), pady=20)
        self.entry.focus()
        
        # Button frame
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.grid(row=0, column=2, padx=(0, 20), pady=20)
        
        self.search_button = ctk.CTkButton(button_frame, text="🔍 Find Alternatives", 
                                         command=self.start_scraping, height=40,
                                         font=ctk.CTkFont(size=12, weight="bold"))
        self.search_button.grid(row=0, column=0, padx=(0, 10))
        
        self.clear_button = ctk.CTkButton(button_frame, text="🗑️ Clear", 
                                        command=self.clear_results, height=40,
                                        fg_color="transparent", border_width=2,
                                        font=ctk.CTkFont(size=12))
        self.clear_button.grid(row=0, column=1)
        
        # Progress section (spans both columns)
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_var = ctk.StringVar(value="Ready to search")
        self.progress_label = ctk.CTkLabel(progress_frame, textvariable=self.progress_var, 
                                         font=ctk.CTkFont(size=12))
        self.progress_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=400, height=15)
        self.progress_bar.grid(row=1, column=0, padx=20, pady=(0, 20))
        self.progress_bar.set(0)  # Hide initially
        
        # Results section
        # Split results section - Left: List, Right: Detail
        # Left side - List view
        list_frame = ctk.CTkFrame(main_frame)
        list_frame.grid(row=3, column=0, sticky="nsew", padx=(0, 10), pady=(0, 20))
        list_frame.grid_rowconfigure(1, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # List control frame
        list_control_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        list_control_frame.grid(row=0, column=0, sticky="ew", pady=(20, 10))
        list_control_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(list_control_frame, text="📋 Alternatives", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w")
        
        self.results_count_var = ctk.StringVar(value="No results")
        results_count_label = ctk.CTkLabel(list_control_frame, textvariable=self.results_count_var, 
                                         font=ctk.CTkFont(size=11), text_color="gray")
        results_count_label.grid(row=0, column=1, sticky="e")
        
        # Material Design List View - Scrollable frame for results
        self.results_scrollable_frame = ctk.CTkScrollableFrame(list_frame, 
                                                            fg_color="transparent",
                                                            corner_radius=0)
        self.results_scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.results_scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Container for list items
        self.results_container = ctk.CTkFrame(self.results_scrollable_frame, 
                                           fg_color="transparent")
        self.results_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initialize empty state
        self.empty_label = ctk.CTkLabel(self.results_container, 
                                      text="🔍 Search for software alternatives to see results here",
                                      font=ctk.CTkFont(size=14, weight="normal"),
                                      text_color="gray")
        self.empty_label.pack(pady=40)
        
        # Right side - Detail view
        detail_frame = ctk.CTkFrame(main_frame)
        detail_frame.grid(row=3, column=1, sticky="nsew", padx=(10, 0), pady=(0, 20))
        detail_frame.grid_rowconfigure(1, weight=1)
        detail_frame.grid_columnconfigure(0, weight=1)
        
        # Detail control frame
        detail_control_frame = ctk.CTkFrame(detail_frame, fg_color="transparent")
        detail_control_frame.grid(row=0, column=0, sticky="ew", pady=(20, 10))
        detail_control_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(detail_control_frame, text="📄 Details", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky="w")
        
        self.export_button = ctk.CTkButton(detail_control_frame, text="💾 Export Results", 
                                         command=self.export_results, height=32,
                                         state="disabled", font=ctk.CTkFont(size=11))
        self.export_button.grid(row=0, column=1, sticky="e")
        
        # Detail view scrollable frame
        self.detail_scrollable_frame = ctk.CTkScrollableFrame(detail_frame, 
                                                            fg_color="transparent",
                                                            corner_radius=0)
        self.detail_scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.detail_scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Container for detail content
        self.detail_container = ctk.CTkFrame(self.detail_scrollable_frame, 
                                          fg_color="transparent")
        self.detail_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initialize detail empty state
        self.detail_empty_label = ctk.CTkLabel(self.detail_container, 
                                             text="👆 Click on an alternative to view details",
                                             font=ctk.CTkFont(size=14, weight="normal"),
                                             text_color="gray")
        self.detail_empty_label.pack(pady=40)
        
        # Status bar (spans both columns)
        self.status_var = ctk.StringVar(value="Ready to search")
        status_bar = ctk.CTkLabel(main_frame, textvariable=self.status_var, 
                                font=ctk.CTkFont(size=10), text_color="gray",
                                fg_color=("gray90", "gray20"), corner_radius=0)
        status_bar.grid(row=4, column=0, columnspan=2, sticky="ew")
        
        # Bind Enter key to search
        self.entry.bind('<Return>', lambda e: self.start_scraping())
        
        # Threading
        self.scraping_thread = None
        self.is_scraping = False
        self.current_alternatives = []
        self.list_items = []  # Store references to list item widgets
        self.detail_items = []  # Store references to detail item widgets
        self.selected_alternative = None  # Currently selected alternative

    def start_scraping(self):
        if self.is_scraping:
            return
            
        software_name = self.entry.get().strip()
        if not software_name:
            messagebox.showwarning("Input Required", "Please enter a software name to search for.")
            self.entry.focus()
            return
        
        # Start scraping in separate thread
        self.is_scraping = True
        self.search_button.configure(state="disabled", text="🔄 Searching...")
        self.clear_button.configure(state="disabled")
        self.progress_var.set("🔍 Searching for alternatives...")
        self.progress_bar.set(0.3)
        self.status_var.set(f"Searching for alternatives to '{software_name}'...")
        # Clear previous results and show loading
        self.clear_list_items()
        if hasattr(self, 'empty_label'):
            self.empty_label.destroy()
        
        loading_label = ctk.CTkLabel(self.results_container, 
                                   text="🔄 Searching for alternatives...",
                                   font=ctk.CTkFont(size=14, weight="normal"),
                                   text_color="gray")
        loading_label.pack(pady=40)
        self.list_items.append(loading_label)
        
        self.export_button.configure(state="disabled")
        self.results_count_var.set("Searching...")
        
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
        self.search_button.configure(state="normal", text="🔍 Find Alternatives")
        self.clear_button.configure(state="normal")
        self.progress_bar.set(0)
        self.progress_var.set("✅ Search completed")
        self.status_var.set("Ready to search")

    def clear_results(self):
        self.clear_list_items()
        self.clear_detail_items()
        # Show empty state
        self.empty_label = ctk.CTkLabel(self.results_container, 
                                      text="🔍 Search for software alternatives to see results here",
                                      font=ctk.CTkFont(size=14, weight="normal"),
                                      text_color="gray")
        self.empty_label.pack(pady=40)
        
        # Reset detail view
        self.detail_empty_label = ctk.CTkLabel(self.detail_container, 
                                             text="👆 Click on an alternative to view details",
                                             font=ctk.CTkFont(size=14, weight="normal"),
                                             text_color="gray")
        self.detail_empty_label.pack(pady=40)
        
        self.results_count_var.set("No results")
        self.export_button.configure(state="disabled")
        self.current_alternatives = []
        self.selected_alternative = None
        self.progress_var.set("Results cleared")
        self.status_var.set("Ready to search")

    def export_results(self):
        if not self.current_alternatives:
            messagebox.showinfo("No Results", "No results to export.")
            return
        
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Results"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    if file_path.endswith('.csv'):
                        f.write("Software Name,Description,URL\n")
                        for alt in self.current_alternatives:
                            f.write(f'"{alt["name"]}","{alt["description"]}","{alt["url"]}"\n')
                    else:
                        f.write(f"Alternatives Found: {len(self.current_alternatives)}\n\n")
                        for i, alt in enumerate(self.current_alternatives, 1):
                            f.write(f"{i}. {alt['name']}\n")
                            if alt['description']:
                                f.write(f"   Description: {alt['description']}\n")
                            if alt['url']:
                                f.write(f"   URL: {alt['url']}\n")
                            f.write("\n")
                
                messagebox.showinfo("Export Successful", f"Results exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export results: {str(e)}")

    def scrape(self, software_name):
        try:
            from selenium import webdriver
            from selenium.webdriver.firefox.options import Options
            from selenium.webdriver.firefox.service import Service
            from webdriver_manager.firefox import GeckoDriverManager
            from bs4 import BeautifulSoup

            # Update status
            self.after(0, lambda: self.progress_var.set("🚀 Initializing browser..."))
            self.after(0, lambda: self.progress_bar.set(0.1))
            
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
            self.after(0, lambda: self.progress_var.set("🌐 Loading webpage..."))
            self.after(0, lambda: self.progress_bar.set(0.4))
            
            url = f'https://alternativeto.net/browse/search?q={software_name}'
            driver.get(url)
            
            # Update status
            self.after(0, lambda: self.progress_var.set("🔍 Parsing content..."))
            self.after(0, lambda: self.progress_bar.set(0.7))
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()

            # Debug: Save HTML for inspection
            with open('debug_page.html', 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            
            # Debug: Log page title and basic info
            title = soup.find('title')
            page_title = title.get_text() if title else "No title found"
            self.after(0, lambda title=page_title: self.progress_var.set(f"📄 Page loaded: {title}"))
            
            # Parse alternatives - updated for current alternativeto.net structure
            alternatives = []
            
            # Method 1: Look for app item containers with data-testid
            app_items = soup.find_all('li', {'data-testid': re.compile(r'^item-')})
            self.after(0, lambda count=len(app_items): self.progress_var.set(f"📱 Found {count} app items"))
            self.after(0, lambda: self.progress_bar.set(0.8))
            
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
                    
                    # Find URL from
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
                self.after(0, lambda: self.progress_var.set("🔄 Trying alternative parsing method..."))
                
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
                self.after(0, lambda: self.progress_var.set("🔍 Trying broad search..."))
                
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
            self.after(0, lambda alts=unique_alternatives, name=software_name: self.update_results(alts, name))

        except Exception as e:
            error_msg = str(e)
            self.after(0, lambda: self.show_error(error_msg))

    def update_results(self, alternatives, software_name):
        # Clear previous content
        self.clear_list_items()
        if hasattr(self, 'empty_label'):
            self.empty_label.destroy()
        
        self.current_alternatives = alternatives
        
        if alternatives:
            # Create title
            title_frame = ctk.CTkFrame(self.results_container, fg_color="transparent")
            title_frame.pack(fill="x", padx=5, pady=(10, 15))
            
            title_label = ctk.CTkLabel(title_frame, 
                                     text=f"🔍 Alternatives to '{software_name}'",
                                     font=ctk.CTkFont(size=16, weight="bold"))
            title_label.pack(anchor="w")
            
            # Create list items for each alternative
            for i, alt in enumerate(alternatives[:15], 1):
                list_item = self.create_list_item(alt, i)
                self.list_items.append(list_item)
            
            self.progress_var.set(f"✅ Found {len(alternatives)} alternatives")
            self.results_count_var.set(f"Found {len(alternatives)} results")
            self.export_button.configure(state="normal")
        else:
            # No results found
            no_results_frame = ctk.CTkFrame(self.results_container, 
                                          corner_radius=12,
                                          fg_color=("gray95", "gray15"),
                                          border_width=1,
                                          border_color=("gray85", "gray25"))
            no_results_frame.pack(fill="x", padx=5, pady=20)
            
            no_results_label = ctk.CTkLabel(no_results_frame, 
                                          text=f"❌ No alternatives found for '{software_name}'",
                                          font=ctk.CTkFont(size=14, weight="bold"),
                                          text_color=("gray70", "gray40"))
            no_results_label.pack(pady=20, padx=20)
            
            reasons_label = ctk.CTkLabel(no_results_frame, 
                                       text="Possible reasons:\n• Website structure may have changed\n• Anti-bot protection active\n• No alternatives available for this software",
                                       font=ctk.CTkFont(size=11),
                                       text_color=("gray60", "gray50"),
                                       justify="left")
            reasons_label.pack(pady=(0, 20), padx=20, anchor="w")
            
            debug_label = ctk.CTkLabel(no_results_frame, 
                                     text="💡 Debug file saved as 'debug_page.html' for inspection",
                                     font=ctk.CTkFont(size=10),
                                     text_color=("gray50", "gray60"))
            debug_label.pack(pady=(0, 20), padx=20, anchor="w")
            
            self.list_items.append(no_results_frame)
            self.progress_var.set("❌ No alternatives found")
            self.results_count_var.set("No results found")
            self.export_button.configure(state="disabled")

    def show_error(self, error_msg):
        # Clear previous content
        self.clear_list_items()
        if hasattr(self, 'empty_label'):
            self.empty_label.destroy()
        
        # Create error display
        error_frame = ctk.CTkFrame(self.results_container, 
                                 corner_radius=12,
                                 fg_color=("lightcoral", "darkred"),
                                 border_width=1,
                                 border_color=("red", "red"))
        error_frame.pack(fill="x", padx=5, pady=20)
        
        error_title = ctk.CTkLabel(error_frame, 
                                 text="❌ Error occurred",
                                 font=ctk.CTkFont(size=14, weight="bold"),
                                 text_color="white")
        error_title.pack(pady=(20, 10), padx=20, anchor="w")
        
        error_content = ctk.CTkLabel(error_frame, 
                                   text=error_msg,
                                   font=ctk.CTkFont(size=11),
                                   text_color="white",
                                   wraplength=400,
                                   justify="left")
        error_content.pack(pady=(0, 10), padx=20, anchor="w")
        
        debug_label = ctk.CTkLabel(error_frame, 
                                 text="💡 Debug file saved as 'debug_page.html' for inspection",
                                 font=ctk.CTkFont(size=10),
                                 text_color=("lightgray", "gray"))
        debug_label.pack(pady=(0, 20), padx=20, anchor="w")
        
        self.list_items.append(error_frame)
        self.progress_var.set("❌ Error occurred")
        self.results_count_var.set("Error")
        self.export_button.configure(state="disabled")

    def create_list_item(self, alternative, index):
        """Create a Material Design-inspired list item"""
        # Main item frame (card-like appearance)
        item_frame = ctk.CTkFrame(self.results_container, 
                                corner_radius=12,
                                fg_color=("gray95", "gray15"),
                                border_width=1,
                                border_color=("gray85", "gray25"))
        item_frame.pack(fill="x", padx=5, pady=3)
        item_frame.grid_columnconfigure(1, weight=1)
        
        # Store alternative data with the frame
        item_frame.alternative = alternative
        
        # Index number
        index_label = ctk.CTkLabel(item_frame, 
                                 text=f"{index}",
                                 font=ctk.CTkFont(size=12, weight="bold"),
                                 text_color=("gray60", "gray50"),
                                 width=30)
        index_label.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="n")
        
        # Content frame
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.grid(row=0, column=1, sticky="ew", padx=(0, 15), pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Software name
        name_label = ctk.CTkLabel(content_frame, 
                                text=alternative['name'],
                                font=ctk.CTkFont(size=14, weight="bold"),
                                anchor="w",
                                justify="left")
        name_label.grid(row=0, column=0, sticky="ew", pady=(0, 3))
        
        # Description
        if alternative['description']:
            desc_label = ctk.CTkLabel(content_frame, 
                                    text=alternative['description'][:100] + "..." if len(alternative['description']) > 100 else alternative['description'],
                                    font=ctk.CTkFont(size=11),
                                    text_color=("gray60", "gray50"),
                                    anchor="w",
                                    justify="left",
                                    wraplength=400)
            desc_label.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        
        # URL
        if alternative['url']:
            url_label = ctk.CTkLabel(content_frame, 
                                   text=f"🔗 {alternative['url']}",
                                   font=ctk.CTkFont(size=10, weight="normal"),
                                   text_color=("blue", "lightblue"),
                                   anchor="w",
                                   justify="left",
                                   cursor="hand2")
            url_label.grid(row=2, column=0, sticky="ew")
            
            # Make URL clickable to open in browser
            url_label.bind("<Button-1>", lambda e, url=alternative['url']: self.open_url(url))
            url_label.bind("<Enter>", lambda e: url_label.configure(text_color=("darkblue", "cyan")))
            url_label.bind("<Leave>", lambda e: url_label.configure(text_color=("blue", "lightblue")))
        
        # Hover effect for the entire item
        def on_enter(e):
            if self.selected_alternative != alternative:
                item_frame.configure(fg_color=("gray90", "gray20"),
                                   border_color=("gray70", "gray30"))
        
        def on_leave(e):
            if self.selected_alternative != alternative:
                item_frame.configure(fg_color=("gray95", "gray15"),
                                   border_color=("gray85", "gray25"))
        
        def on_click(e):
            self.select_alternative(alternative, item_frame)
        
        item_frame.bind("<Enter>", on_enter)
        item_frame.bind("<Leave>", on_leave)
        item_frame.bind("<Button-1>", on_click)
        item_frame.configure(cursor="hand2")
        
        return item_frame

    def select_alternative(self, alternative, item_frame):
        """Handle alternative selection and load details"""
        # Update selection state
        self.selected_alternative = alternative
        
        # Update visual selection
        self.update_list_selection()
        
        # Load detailed information
        self.load_alternative_details(alternative)

    def update_list_selection(self):
        """Update visual selection state of list items"""
        for item in self.list_items:
            if hasattr(item, 'alternative') and item.alternative == self.selected_alternative:
                item.configure(fg_color=("lightblue", "darkblue"),
                             border_color=("blue", "lightblue"))
            else:
                item.configure(fg_color=("gray95", "gray15"),
                             border_color=("gray85", "gray25"))

    def load_alternative_details(self, alternative):
        """Load and display detailed information for the selected alternative"""
        # Clear previous detail content
        self.clear_detail_items()
        
        # Show loading state
        loading_label = ctk.CTkLabel(self.detail_container, 
                                   text="🔄 Loading details...",
                                   font=ctk.CTkFont(size=14, weight="normal"),
                                   text_color="gray")
        loading_label.pack(pady=40)
        self.detail_items.append(loading_label)
        
        # Start detail scraping in separate thread
        detail_thread = threading.Thread(target=self.scrape_alternative_details, args=(alternative,))
        detail_thread.daemon = True
        detail_thread.start()

    def scrape_alternative_details(self, alternative):
        """Scrape detailed information from the alternative's page"""
        try:
            from selenium import webdriver
            from selenium.webdriver.firefox.options import Options
            from selenium.webdriver.firefox.service import Service
            from webdriver_manager.firefox import GeckoDriverManager
            from bs4 import BeautifulSoup

            # Update status
            self.after(0, lambda: self.status_var.set(f"Loading details for {alternative['name']}..."))
            
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
            
            # Construct the about page URL
            software_name = alternative['name'].lower()
            # Clean the name for URL: replace spaces with hyphens, remove special characters
            software_name = re.sub(r'[^a-z0-9\s-]', '', software_name)  # Remove special chars except spaces and hyphens
            software_name = re.sub(r'\s+', '-', software_name)  # Replace spaces with hyphens
            software_name = re.sub(r'-+', '-', software_name)  # Replace multiple hyphens with single
            software_name = software_name.strip('-')  # Remove leading/trailing hyphens
            
            about_url = f"https://alternativeto.net/software/{software_name}/about/"
            
            # Update status with the URL being used
            self.after(0, lambda url=about_url: self.status_var.set(f"Loading: {url}"))
            
            # Load the alternative's about page
            driver.get(about_url)
            
            # Parse the page content
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()

            # Extract detailed information
            details = self.parse_alternative_details(soup, alternative)
            
            # Update the URL in details to point to the about page
            details['url'] = about_url
            
            # Update the detail view
            self.after(0, lambda: self.display_alternative_details(details))

        except Exception as e:
            error_msg = str(e)
            self.after(0, lambda: self.show_detail_error(error_msg))

    def parse_alternative_details(self, soup, alternative):
        """Parse detailed information from the alternative's page"""
        details = {
            'name': alternative['name'],
            'url': alternative['url'],
            'description': '',
            'features': [],
            'screenshots': [],
            'rating': '',
            'license': '',
            'platforms': [],
            'categories': [],
            'developer': '',
            'website': '',
            'version': '',
            'last_updated': '',
            'file_size': '',
            'languages': [],
            'system_requirements': '',
            'pros': [],
            'cons': [],
            'user_reviews': '',
            'downloads': '',
            'support_info': '',
            'similar_alternatives': [],
            'brand_box_items': [],
            'popular_alternatives': [],
            'box_categories': []
        }
        
        try:
            # Extract detailed description
            desc_selectors = [
                'meta[name="description"]',
                '.app-description',
                '.description',
                '[data-testid="description"]',
                '.summary',
                '.app-summary',
                '.overview'
            ]
            
            for selector in desc_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    if desc_elem.name == 'meta':
                        details['description'] = desc_elem.get('content', '')
                    else:
                        details['description'] = desc_elem.get_text(strip=True)
                    break
            
            # Extract features/benefits
            feature_selectors = [
                '.features',
                '.benefits',
                '.pros',
                '[data-testid="features"]',
                '.feature-list',
                '.key-features',
                '.what-you-get'
            ]
            
            for selector in feature_selectors:
                feature_elem = soup.select_one(selector)
                if feature_elem:
                    features = feature_elem.find_all(['li', 'p', 'div'])
                    details['features'] = [f.get_text(strip=True) for f in features[:12] if f.get_text(strip=True)]  # Limit to 12
                    break
            
            # Extract rating
            rating_selectors = [
                '.rating',
                '.stars',
                '[data-testid="rating"]',
                '.score',
                '.user-rating',
                '.average-rating'
            ]
            
            for selector in rating_selectors:
                rating_elem = soup.select_one(selector)
                if rating_elem:
                    details['rating'] = rating_elem.get_text(strip=True)
                    break
            
            # Extract license information
            license_selectors = [
                '.license',
                '.pricing',
                '[data-testid="license"]',
                '.price',
                '.cost'
            ]
            
            for selector in license_selectors:
                license_elem = soup.select_one(selector)
                if license_elem:
                    details['license'] = license_elem.get_text(strip=True)
                    break
            
            # Extract platforms
            platform_selectors = [
                '.platforms',
                '.os',
                '[data-testid="platforms"]',
                '.operating-systems',
                '.supported-platforms'
            ]
            
            for selector in platform_selectors:
                platform_elem = soup.select_one(selector)
                if platform_elem:
                    platforms = platform_elem.find_all(['li', 'span', 'div'])
                    details['platforms'] = [p.get_text(strip=True) for p in platforms[:10] if p.get_text(strip=True)]
                    break
            
            # Extract categories
            category_selectors = [
                '.categories',
                '.tags',
                '[data-testid="categories"]',
                '.category-list',
                '.topics'
            ]
            
            for selector in category_selectors:
                category_elem = soup.select_one(selector)
                if category_elem:
                    categories = category_elem.find_all(['li', 'span', 'a', 'div'])
                    details['categories'] = [c.get_text(strip=True) for c in categories[:15] if c.get_text(strip=True)]
                    break
            
            # Extract developer information
            developer_selectors = [
                '.developer',
                '.author',
                '[data-testid="developer"]',
                '.publisher',
                '.company'
            ]
            
            for selector in developer_selectors:
                developer_elem = soup.select_one(selector)
                if developer_elem:
                    details['developer'] = developer_elem.get_text(strip=True)
                    break
            
            # Extract official website
            website_selectors = [
                '.website',
                '.homepage',
                '[data-testid="website"]',
                'a[href*="http"]'
            ]
            
            for selector in website_selectors:
                website_elem = soup.select_one(selector)
                if website_elem and website_elem.get('href'):
                    href = website_elem.get('href')
                    if href.startswith('http') and 'alternativeto.net' not in href:
                        details['website'] = href
                        break
            
            # Extract version information
            version_selectors = [
                '.version',
                '[data-testid="version"]',
                '.current-version',
                '.latest-version',
                '.release-version'
            ]
            
            for selector in version_selectors:
                version_elem = soup.select_one(selector)
                if version_elem:
                    details['version'] = version_elem.get_text(strip=True)
                    break
            
            # Extract last updated date
            updated_selectors = [
                '.last-updated',
                '.updated',
                '[data-testid="updated"]',
                '.release-date',
                '.date'
            ]
            
            for selector in updated_selectors:
                updated_elem = soup.select_one(selector)
                if updated_elem:
                    details['last_updated'] = updated_elem.get_text(strip=True)
                    break
            
            # Extract file size
            size_selectors = [
                '.file-size',
                '.size',
                '[data-testid="size"]',
                '.download-size'
            ]
            
            for selector in size_selectors:
                size_elem = soup.select_one(selector)
                if size_elem:
                    details['file_size'] = size_elem.get_text(strip=True)
                    break
            
            # Extract languages
            language_selectors = [
                '.languages',
                '.supported-languages',
                '[data-testid="languages"]',
                '.localization'
            ]
            
            for selector in language_selectors:
                language_elem = soup.select_one(selector)
                if language_elem:
                    languages = language_elem.find_all(['li', 'span', 'div'])
                    details['languages'] = [l.get_text(strip=True) for l in languages[:10] if l.get_text(strip=True)]
                    break
            
            # Extract system requirements
            requirements_selectors = [
                '.requirements',
                '.system-requirements',
                '[data-testid="requirements"]',
                '.specs',
                '.minimum-requirements'
            ]
            
            for selector in requirements_selectors:
                req_elem = soup.select_one(selector)
                if req_elem:
                    details['system_requirements'] = req_elem.get_text(strip=True)
                    break
            
            # Extract pros
            pros_selectors = [
                '.pros',
                '.advantages',
                '[data-testid="pros"]',
                '.positives'
            ]
            
            for selector in pros_selectors:
                pros_elem = soup.select_one(selector)
                if pros_elem:
                    pros = pros_elem.find_all(['li', 'p', 'div'])
                    details['pros'] = [p.get_text(strip=True) for p in pros[:8] if p.get_text(strip=True)]
                    break
            
            # Extract cons
            cons_selectors = [
                '.cons',
                '.disadvantages',
                '[data-testid="cons"]',
                '.negatives',
                '.drawbacks'
            ]
            
            for selector in cons_selectors:
                cons_elem = soup.select_one(selector)
                if cons_elem:
                    cons = cons_elem.find_all(['li', 'p', 'div'])
                    details['cons'] = [c.get_text(strip=True) for c in cons[:8] if c.get_text(strip=True)]
                    break
            
            # Extract user reviews count
            reviews_selectors = [
                '.reviews-count',
                '.user-reviews',
                '[data-testid="reviews"]',
                '.review-count'
            ]
            
            for selector in reviews_selectors:
                reviews_elem = soup.select_one(selector)
                if reviews_elem:
                    details['user_reviews'] = reviews_elem.get_text(strip=True)
                    break
            
            # Extract downloads count
            downloads_selectors = [
                '.downloads',
                '.download-count',
                '[data-testid="downloads"]',
                '.installs'
            ]
            
            for selector in downloads_selectors:
                downloads_elem = soup.select_one(selector)
                if downloads_elem:
                    details['downloads'] = downloads_elem.get_text(strip=True)
                    break
            
            # Extract support information
            support_selectors = [
                '.support',
                '.help',
                '[data-testid="support"]',
                '.contact',
                '.technical-support'
            ]
            
            for selector in support_selectors:
                support_elem = soup.select_one(selector)
                if support_elem:
                    details['support_info'] = support_elem.get_text(strip=True)
                    break
            
            # Extract similar alternatives
            similar_selectors = [
                '.similar',
                '.alternatives',
                '[data-testid="similar"]',
                '.related-software',
                '.also-like'
            ]
            
            for selector in similar_selectors:
                similar_elem = soup.select_one(selector)
                if similar_elem:
                    similar = similar_elem.find_all(['li', 'a', 'div'])
                    details['similar_alternatives'] = [s.get_text(strip=True) for s in similar[:6] if s.get_text(strip=True)]
                    break
            
            # Extract items from Box_brandBox container
            brand_box_selectors = [
                '.Box_box__20D8q.Box_brandBox__v0VQV.commonBoxList',
                '.Box_brandBox__v0VQV',
                '.commonBoxList',
                '[class*="Box_brandBox"]',
                '[class*="commonBoxList"]'
            ]
            
            for selector in brand_box_selectors:
                brand_box_elem = soup.select_one(selector)
                if brand_box_elem:
                    # Extract popular alternatives with links
                    popular_alternatives = []
                    alternative_links = brand_box_elem.find_all('a', href=re.compile(r'/software/'))
                    
                    for link in alternative_links[:10]:  # Limit to 10 alternatives
                        alt_name = link.get_text(strip=True)
                        alt_url = link.get('href')
                        if alt_name and alt_url and len(alt_name) > 1:
                            if alt_url.startswith('/'):
                                alt_url = f"https://alternativeto.net{alt_url}"
                            popular_alternatives.append({
                                'name': alt_name,
                                'url': alt_url
                            })
                    
                    # Extract categories from the brand box
                    categories_in_box = []
                    category_selectors = [
                        '.category',
                        '.tag',
                        '[class*="category"]',
                        '[class*="tag"]'
                    ]
                    
                    for cat_selector in category_selectors:
                        cat_elements = brand_box_elem.select(cat_selector)
                        for cat_elem in cat_elements[:8]:  # Limit to 8 categories
                            cat_text = cat_elem.get_text(strip=True)
                            if cat_text and len(cat_text) > 1 and cat_text not in categories_in_box:
                                categories_in_box.append(cat_text)
                    
                    # Also look for any list items that might be categories
                    list_items = brand_box_elem.find_all('li')
                    for li in list_items[:5]:  # Check first 5 list items
                        li_text = li.get_text(strip=True)
                        if li_text and len(li_text) > 1 and li_text not in categories_in_box:
                            categories_in_box.append(li_text)
                    
                    # Store the extracted data
                    if popular_alternatives:
                        details['popular_alternatives'] = popular_alternatives
                    
                    if categories_in_box:
                        details['box_categories'] = categories_in_box
                    
                    break
        
        except Exception as e:
            print(f"Error parsing details: {e}")
        
        return details

    def display_alternative_details(self, details):
        """Display the parsed alternative details in Material Design format"""
        # Clear previous content
        self.clear_detail_items()
        
        # Create header
        header_frame = ctk.CTkFrame(self.detail_container, 
                                  corner_radius=12,
                                  fg_color=("lightblue", "darkblue"),
                                  border_width=1,
                                  border_color=("blue", "lightblue"))
        header_frame.pack(fill="x", padx=5, pady=(10, 15))
        
        title_label = ctk.CTkLabel(header_frame, 
                                 text=f"📱 {details['name']}",
                                 font=ctk.CTkFont(size=16, weight="bold"),
                                 text_color="white")
        title_label.pack(pady=15, padx=20)
        
        self.detail_items.append(header_frame)
        
        # Description section
        if details['description']:
            desc_frame = self.create_detail_section("📝 Description", details['description'])
            self.detail_items.append(desc_frame)
        
        # Rating section
        if details['rating']:
            rating_frame = self.create_detail_section("⭐ Rating", details['rating'])
            self.detail_items.append(rating_frame)
        
        # Version section
        if details['version']:
            version_frame = self.create_detail_section("🔢 Version", details['version'])
            self.detail_items.append(version_frame)
        
        # Last Updated section
        if details['last_updated']:
            updated_frame = self.create_detail_section("📅 Last Updated", details['last_updated'])
            self.detail_items.append(updated_frame)
        
        # File Size section
        if details['file_size']:
            size_frame = self.create_detail_section("💾 File Size", details['file_size'])
            self.detail_items.append(size_frame)
        
        # License section
        if details['license']:
            license_frame = self.create_detail_section("💰 License", details['license'])
            self.detail_items.append(license_frame)
        
        # Platforms section
        if details['platforms']:
            platforms_text = "\n".join(f"• {platform}" for platform in details['platforms'])
            platforms_frame = self.create_detail_section("🖥️ Platforms", platforms_text)
            self.detail_items.append(platforms_frame)
        
        # Languages section
        if details['languages']:
            languages_text = ", ".join(details['languages'])
            languages_frame = self.create_detail_section("🌍 Languages", languages_text)
            self.detail_items.append(languages_frame)
        
        # System Requirements section
        if details['system_requirements']:
            req_frame = self.create_detail_section("⚙️ System Requirements", details['system_requirements'])
            self.detail_items.append(req_frame)
        
        # Features section
        if details['features']:
            features_text = "\n".join(f"• {feature}" for feature in details['features'])
            features_frame = self.create_detail_section("✨ Features", features_text)
            self.detail_items.append(features_frame)
        
        # Pros section
        if details['pros']:
            pros_text = "\n".join(f"✅ {pro}" for pro in details['pros'])
            pros_frame = self.create_detail_section("👍 Pros", pros_text)
            self.detail_items.append(pros_frame)
        
        # Cons section
        if details['cons']:
            cons_text = "\n".join(f"❌ {con}" for con in details['cons'])
            cons_frame = self.create_detail_section("👎 Cons", cons_text)
            self.detail_items.append(cons_frame)
        
        # Categories section
        if details['categories']:
            categories_text = ", ".join(details['categories'])
            categories_frame = self.create_detail_section("🏷️ Categories", categories_text)
            self.detail_items.append(categories_frame)
        
        # User Reviews section
        if details['user_reviews']:
            reviews_frame = self.create_detail_section("💬 User Reviews", details['user_reviews'])
            self.detail_items.append(reviews_frame)
        
        # Downloads section
        if details['downloads']:
            downloads_frame = self.create_detail_section("⬇️ Downloads", details['downloads'])
            self.detail_items.append(downloads_frame)
        
        # Developer section
        if details['developer']:
            developer_frame = self.create_detail_section("👨‍💻 Developer", details['developer'])
            self.detail_items.append(developer_frame)
        
        # Support Info section
        if details['support_info']:
            support_frame = self.create_detail_section("🆘 Support", details['support_info'])
            self.detail_items.append(support_frame)
        
        # Similar Alternatives section
        if details['similar_alternatives']:
            similar_text = "\n".join(f"• {alt}" for alt in details['similar_alternatives'])
            similar_frame = self.create_detail_section("🔄 Similar Alternatives", similar_text)
            self.detail_items.append(similar_frame)
        
        # Brand Box Items section
        if details['brand_box_items']:
            brand_text = "\n".join(f"• {item}" for item in details['brand_box_items'])
            brand_frame = self.create_detail_section("📦 Brand Box Items", brand_text)
            self.detail_items.append(brand_frame)
        
        # Popular Alternatives section
        if details['popular_alternatives']:
            alt_text = "\n".join(f"• {alt['name']}" for alt in details['popular_alternatives'])
            alt_frame = self.create_detail_section("🔥 Popular Alternatives", alt_text)
            self.detail_items.append(alt_frame)
        
        # Box Categories section
        if details['box_categories']:
            box_cat_text = ", ".join(details['box_categories'])
            box_cat_frame = self.create_detail_section("📂 Box Categories", box_cat_text)
            self.detail_items.append(box_cat_frame)
        
        # Links section
        links_frame = ctk.CTkFrame(self.detail_container, 
                                 corner_radius=12,
                                 fg_color=("gray95", "gray15"),
                                 border_width=1,
                                 border_color=("gray85", "gray25"))
        links_frame.pack(fill="x", padx=5, pady=10)
        
        links_title = ctk.CTkLabel(links_frame, 
                                 text="🔗 Links",
                                 font=ctk.CTkFont(size=14, weight="bold"))
        links_title.pack(pady=(15, 10), padx=20, anchor="w")
        
        # AlternativeTo.net link
        if details['url']:
            altto_button = ctk.CTkButton(links_frame, 
                                       text="🔍 View on AlternativeTo.net",
                                       command=lambda: self.open_url(details['url']),
                                       height=35,
                                       font=ctk.CTkFont(size=11))
            altto_button.pack(pady=(0, 10), padx=20, fill="x")
        
        # Popular Alternatives Links
        if details['popular_alternatives']:
            for alt in details['popular_alternatives'][:5]:  # Show first 5 popular alternatives as buttons
                alt_button = ctk.CTkButton(links_frame, 
                                         text=f"🔗 {alt['name']}",
                                         command=lambda url=alt['url']: self.open_url(url),
                                         height=30,
                                         font=ctk.CTkFont(size=10),
                                         fg_color="transparent",
                                         border_width=1)
                alt_button.pack(pady=(0, 5), padx=20, fill="x")
        
        # Official website link
        if details['website']:
            website_button = ctk.CTkButton(links_frame, 
                                         text="🌐 Official Website",
                                         command=lambda: self.open_url(details['website']),
                                         height=35,
                                         fg_color="transparent",
                                         border_width=2,
                                         font=ctk.CTkFont(size=11))
            website_button.pack(pady=(0, 15), padx=20, fill="x")
        
        self.detail_items.append(links_frame)
        
        # Update status
        self.status_var.set("Ready to search")

    def create_detail_section(self, title, content):
        """Create a Material Design detail section"""
        section_frame = ctk.CTkFrame(self.detail_container, 
                                   corner_radius=12,
                                   fg_color=("gray95", "gray15"),
                                   border_width=1,
                                   border_color=("gray85", "gray25"))
        section_frame.pack(fill="x", padx=5, pady=5)
        
        title_label = ctk.CTkLabel(section_frame, 
                                 text=title,
                                 font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(pady=(15, 10), padx=20, anchor="w")
        
        content_label = ctk.CTkLabel(section_frame, 
                                   text=content,
                                   font=ctk.CTkFont(size=11),
                                   text_color=("gray60", "gray50"),
                                   wraplength=350,
                                   justify="left")
        content_label.pack(pady=(0, 15), padx=20, anchor="w")
        
        return section_frame

    def show_detail_error(self, error_msg):
        """Show error in detail view"""
        self.clear_detail_items()
        
        error_frame = ctk.CTkFrame(self.detail_container, 
                                 corner_radius=12,
                                 fg_color=("lightcoral", "darkred"),
                                 border_width=1,
                                 border_color=("red", "red"))
        error_frame.pack(fill="x", padx=5, pady=20)
        
        error_title = ctk.CTkLabel(error_frame, 
                                 text="❌ Failed to load details",
                                 font=ctk.CTkFont(size=14, weight="bold"),
                                 text_color="white")
        error_title.pack(pady=(20, 10), padx=20, anchor="w")
        
        error_content = ctk.CTkLabel(error_frame, 
                                   text=error_msg,
                                   font=ctk.CTkFont(size=11),
                                   text_color="white",
                                   wraplength=350,
                                   justify="left")
        error_content.pack(pady=(0, 20), padx=20, anchor="w")
        
        debug_label = ctk.CTkLabel(error_frame, 
                                 text="💡 Debug file saved as 'debug_page.html' for inspection",
                                 font=ctk.CTkFont(size=10),
                                 text_color=("lightgray", "gray"))
        debug_label.pack(pady=(0, 20), padx=20, anchor="w")
        
        self.detail_items.append(error_frame)
        self.status_var.set("Ready to search")

    def clear_detail_items(self):
        """Clear all detail items"""
        for item in self.detail_items:
            item.destroy()
        self.detail_items.clear()

    def clear_list_items(self):
        """Clear all list items"""
        for item in self.list_items:
            item.destroy()
        self.list_items.clear()

    def open_url(self, url):
        """Open URL in default browser"""
        import webbrowser
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Failed to open URL: {e}")

if __name__ == "__main__":
    app = AltScrapBrowser()
    app.mainloop()
