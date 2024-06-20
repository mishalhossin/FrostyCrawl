"""
Common utils used by FrostyCrawl.
"""
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Set

def add_new_urls_to_visit(soup: BeautifulSoup, current_url: str, to_visit: Set[str], visited: Set[str]) -> None:
    for link in soup.find_all(name="a", href=True):
        href = urljoin(base=current_url, url=link["href"])
        parsed_href = urlparse(url=href)
        if not parsed_href.fragment and not parsed_href.path.lower().endswith(
            (".pdf", ".jpg", ".png", ".gif")
        ):
            if (
                parsed_href.netloc == urlparse(url=current_url).netloc
                and href not in visited
            ):
                to_visit.add(href)