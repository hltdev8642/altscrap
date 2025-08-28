#!/usr/bin/env python3
"""
Simple test script to verify CustomTkinter installation and basic functionality
"""

import customtkinter as ctk

def test_customtkinter():
    """Test basic CustomTkinter functionality"""
    print("Testing CustomTkinter...")

    # Set appearance
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    # Create main window
    root = ctk.CTk()
    root.title("CustomTkinter Test")
    root.geometry("400x300")

    # Create a simple label
    label = ctk.CTkLabel(root, text="✅ CustomTkinter is working!", font=ctk.CTkFont(size=16, weight="bold"))
    label.pack(pady=20)

    # Create a button
    button = ctk.CTkButton(root, text="Test Button", command=lambda: print("Button clicked!"))
    button.pack(pady=10)

    # Create a frame
    frame = ctk.CTkFrame(root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    inner_label = ctk.CTkLabel(frame, text="This is inside a frame")
    inner_label.pack(pady=10)

    print("✅ CustomTkinter test window created successfully")
    print("✅ All widgets created without errors")

    # Don't show the window, just test creation
    root.destroy()
    print("✅ Test completed successfully")

if __name__ == "__main__":
    test_customtkinter()
