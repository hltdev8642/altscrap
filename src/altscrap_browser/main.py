import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import threading
import os

# Set CustomTkinter appearance
ctk.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class AltScrapBrowser(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🔍 AlternativeTo.net Browser")
        self.geometry("900x700")
        self.resizable(True, True)
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header section
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(header_frame, text="🔍 AlternativeTo.net Browser", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        subtitle_label = ctk.CTkLabel(header_frame, text="Find alternative software solutions", 
                                     font=ctk.CTkFont(size=12), text_color="gray")
        subtitle_label.grid(row=1, column=0)
        
        # Input section
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
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
        
        # Progress section
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_var = ctk.StringVar(value="Ready to search")
        self.progress_label = ctk.CTkLabel(progress_frame, textvariable=self.progress_var, 
                                         font=ctk.CTkFont(size=12))
        self.progress_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=400, height=15)
        self.progress_bar.grid(row=1, column=0, padx=20, pady=(0, 20))
        self.progress_bar.set(0)  # Hide initially
        
        # Results section
        results_frame = ctk.CTkFrame(main_frame)
        results_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 20))
        results_frame.grid_rowconfigure(1, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Results control frame
        results_control_frame = ctk.CTkFrame(results_frame, fg_color="transparent")
        results_control_frame.grid(row=0, column=0, sticky="ew", pady=(20, 10))
        results_control_frame.grid_columnconfigure(0, weight=1)
        
        self.results_count_var = ctk.StringVar(value="No results")
        results_count_label = ctk.CTkLabel(results_control_frame, textvariable=self.results_count_var, 
                                         font=ctk.CTkFont(size=11), text_color="gray")
        results_count_label.grid(row=0, column=0, sticky="w")
        
        self.export_button = ctk.CTkButton(results_control_frame, text="💾 Export Results", 
                                         command=self.export_results, height=32,
                                         state="disabled", font=ctk.CTkFont(size=11))
        self.export_button.grid(row=0, column=1, sticky="e")
        
        # Material Design List View - Scrollable frame for results
        self.results_scrollable_frame = ctk.CTkScrollableFrame(results_frame, 
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
        
        # Status bar
        self.status_var = ctk.StringVar(value="Ready to search")
        status_bar = ctk.CTkLabel(main_frame, textvariable=self.status_var, 
                                font=ctk.CTkFont(size=10), text_color="gray",
                                fg_color=("gray90", "gray20"), corner_radius=0)
        status_bar.grid(row=4, column=0, sticky="ew")
        
        # Bind Enter key to search
        self.entry.bind('<Return>', lambda e: self.start_scraping())
        
        # Threading
        self.scraping_thread = None
        self.is_scraping = False
        self.current_alternatives = []
        self.list_items = []  # Store references to list item widgets

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
        # Show empty state
        self.empty_label = ctk.CTkLabel(self.results_container, 
                                      text="🔍 Search for software alternatives to see results here",
                                      font=ctk.CTkFont(size=14, weight="normal"),
                                      text_color="gray")
        self.empty_label.pack(pady=40)
        self.results_count_var.set("No results")
        self.export_button.configure(state="disabled")
        self.current_alternatives = []
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
            import re

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
            
            # Make URL clickable
            url_label.bind("<Button-1>", lambda e, url=alternative['url']: self.open_url(url))
            url_label.bind("<Enter>", lambda e: url_label.configure(text_color=("darkblue", "cyan")))
            url_label.bind("<Leave>", lambda e: url_label.configure(text_color=("blue", "lightblue")))
        
        # Hover effect for the entire item
        def on_enter(e):
            item_frame.configure(fg_color=("gray90", "gray20"),
                               border_color=("gray70", "gray30"))
        
        def on_leave(e):
            item_frame.configure(fg_color=("gray95", "gray15"),
                               border_color=("gray85", "gray25"))
        
        item_frame.bind("<Enter>", on_enter)
        item_frame.bind("<Leave>", on_leave)
        
        # Make the whole item clickable to open URL
        if alternative['url']:
            item_frame.bind("<Button-1>", lambda e, url=alternative['url']: self.open_url(url))
            item_frame.configure(cursor="hand2")
        
        return item_frame

    def open_url(self, url):
        """Open URL in default browser"""
        import webbrowser
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Failed to open URL: {e}")

    def clear_list_items(self):
        """Clear all list items"""
        for item in self.list_items:
            item.destroy()
        self.list_items.clear()

if __name__ == "__main__":
    app = AltScrapBrowser()
    app.mainloop()
