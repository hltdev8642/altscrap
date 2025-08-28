#!/usr/bin/env python3
"""
Demo script to showcase the Material Design list view
"""

import customtkinter as ctk
import webbrowser

class MaterialListDemo(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Material Design List View Demo")
        self.geometry("800x600")

        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Title
        title_label = ctk.CTkLabel(main_frame, text="🎨 Material Design List View",
                                 font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, pady=(20, 10))

        # Scrollable frame for list
        scrollable_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        scrollable_frame.grid_columnconfigure(0, weight=1)

        # Container for list items
        container = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=5, pady=5)

        # Sample data
        sample_alternatives = [
            {
                "name": "Visual Studio Code",
                "description": "A free, open-source code editor with built-in support for debugging, version control, and extensions.",
                "url": "https://code.visualstudio.com/"
            },
            {
                "name": "Sublime Text",
                "description": "A sophisticated text editor for code, markup and prose with a sleek user interface.",
                "url": "https://www.sublimetext.com/"
            },
            {
                "name": "Atom",
                "description": "A hackable text editor for the 21st Century, built on Electron.",
                "url": "https://atom.io/"
            },
            {
                "name": "Notepad++",
                "description": "A free source code editor and Notepad replacement that supports several languages.",
                "url": "https://notepad-plus-plus.org/"
            },
            {
                "name": "Vim",
                "description": "A highly configurable text editor built to make creating and changing any kind of text very efficient.",
                "url": "https://www.vim.org/"
            }
        ]

        # Create list items
        for i, alt in enumerate(sample_alternatives, 1):
            self.create_list_item(container, alt, i)

    def create_list_item(self, container, alternative, index):
        """Create a Material Design-inspired list item"""
        # Main item frame (card-like appearance)
        item_frame = ctk.CTkFrame(container,
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
                                    text=alternative['description'][:120] + "..." if len(alternative['description']) > 120 else alternative['description'],
                                    font=ctk.CTkFont(size=11),
                                    text_color=("gray60", "gray50"),
                                    anchor="w",
                                    justify="left",
                                    wraplength=500)
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

    def open_url(self, url):
        """Open URL in default browser"""
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Failed to open URL: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = MaterialListDemo()
    app.mainloop()
