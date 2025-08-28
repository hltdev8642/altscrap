#!/usr/bin/env python3
"""
Test script to verify urllib3 and requests compatibility
"""

try:
    import urllib3
    print(f"✅ urllib3 version: {urllib3.__version__}")

    import requests
    print(f"✅ requests version: {requests.__version__}")

    # Test the specific import that was failing
    from urllib3.packages.six.moves import urllib
    print("✅ urllib3.packages.six.moves import successful")

    # Test selenium imports
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    print("✅ Selenium imports successful")

    # Test webdriver-manager
    from webdriver_manager.firefox import GeckoDriverManager
    print("✅ webdriver-manager import successful")

    # Test beautifulsoup4
    from bs4 import BeautifulSoup
    print("✅ BeautifulSoup import successful")

    print("\n🎉 All imports successful! The dependency issue is resolved.")

except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
