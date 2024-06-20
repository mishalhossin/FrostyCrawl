import concurrent.futures
from typing import Dict, List, Set

from bs4 import BeautifulSoup

from .scraper import Scraper
from .utils import add_new_urls_to_visit


class WebCrawler:
    def __init__(self) -> None:
        self.visited: Set[str] = set()
        self.results: List[Dict] = []
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        self.scraper = Scraper()

    def crawl_url(self, url: str) -> None:
        to_visit: Set[str] = {url}
        while to_visit:
            current_url = to_visit.pop()
            if current_url in self.visited:
                continue
            html = self.scraper.scrape_html(url=current_url)
            if not html:
                continue
            self.visited.add(current_url)
            print(f"Fetching {current_url}")
            soup = BeautifulSoup(markup=html, features="html.parser")
            self.results.append({"url": current_url, "html": html})
            add_new_urls_to_visit(
                soup=soup,
                current_url=current_url,
                to_visit=to_visit,
                visited=self.visited,
            )

    def save_results(self, filename: str) -> None:
        import json

        with open(file=filename, encoding="utf-8", mode="w") as f:
            f.write(json.dumps(obj=self.results, indent=4))
