import re
from urllib.parse import urljoin

from html2text_rs import html2text


class ScraperExtractor:
    def extract_text_content(self, html_content: str) -> str:
        text = html2text(html_content)
        return text

    def extract_links(self, html_content: str, base_url: str) -> list:
        import bs4

        soup = bs4.BeautifulSoup(html_content, "html.parser")
        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            href = self.make_absolute_url(href, base_url)
            if href:
                links.add(href)
        return list(links)

    def make_absolute_url(self, url: str, base_url: str) -> str:
        if re.match(r"^https?:\/\/", url):
            return url
        return urljoin(base_url, url)
