"""
Scraper class to fetch HTML from a given URL.
"""
from typing import Optional

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Scraper:
    def __init__(self) -> None:
        self.driver = None

    def scrape_html(self, url: str, force_selenium: bool = False) -> Optional[str]:
        html = self._fetch_html_with_requests(url=url)
        if html is None or (self._needs_selenium(html=html) or force_selenium):
            return self._fetch_html_with_selenium(url=url)
        return html

    def _fetch_html_with_requests(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url=url, timeout=10)
            response.raise_for_status()
            if "text/html" in response.headers.get("Content-Type", default=""):
                return response.text
            print(f"Skipped non-HTML content at {url}")
        except requests.RequestException as e:
            print(f"Request failed for {url}: {e}")
        return None

    def _fetch_html_with_selenium(self, url: str) -> str:
        if not self.driver:
            options = Options()
            options.headless = True  # type: ignore
            service = Service(executable_path=ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(url=url)
        html = self.driver.page_source
        return html

    def _needs_selenium(self, html: str) -> bool:
        soup = BeautifulSoup(markup=html, features="html.parser")
        return len(soup.find_all(name="script", attrs={"src": True})) > 5

    def __del__(self):
        if self.driver:
            self.driver.quit()
