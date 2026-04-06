from lxml import html
from lxml.etree import _Element


class SearchResultParser:
    _doc: _Element

    def __init__(self, html_text: str):
        self._doc = html.fromstring(html_text)

    def parse(self):
        rows = self._doc.xpath("//a[@class='grid-card-link url-image']/@href")
        return rows
