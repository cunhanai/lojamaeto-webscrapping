from bs4 import BeautifulSoup
from app.domain.produto import Produto
from lxml import html
from lxml.etree import _Element
import app.scrapping.normalizers as norm


class ProdutoParser:
    _html_text: str
    _soup: BeautifulSoup
    _doc: _Element

    def __init__(self, html_text: str):
        self._html_text = html_text
        self._soup = BeautifulSoup(html_text, "lxml")
        self._doc = html.fromstring(html_text)

    def parse_produto(self) -> Produto:
        """Analisa o HTML de um produto e extrai as informações relevantes para
        criar um objeto de Produto.

        Args:
            html (str): O HTML do produto a ser analisado.

        Returns:
            ProdutoDto: Um objeto ProdutoDto contendo as informações extraídas
            do HTML.
        """
        return Produto(
            sku=self._extract_sku(),
            titulo=self._extract_titulo(),
            preco=self._extract_preco(),
            # preco_pix=preco_pix,
            # valor_parcela=valor_parcela,
            # numero_parcela=numero_parcela,
            # informacoes_tecnicas=informacoes_tecnicas,
        )

    def _extract_sku(self) -> int:
        """Extrai o SKU do produto a partir do HTML.

        Args:
            html (str): O HTML do produto.

        Returns:
            int: O SKU do produto.
        """
        sku_element = self._soup.select_one(".sku-active")

        if sku_element:
            return norm.converter_int(sku_element.text)

        raise ValueError("SKU não encontrado")

    def _extract_titulo(self) -> str:
        """Extrai o título do produto a partir do HTML.

        Args:
            html (str): O HTML do produto.

        Returns:
            str: O título do produto.
        """
        title_element = self._doc.xpath("//h1/span/text()")

        if title_element:
            return norm.normalizar_whitespaces(title_element[0])

        raise ValueError("Título não encontrado")

    def _extract_preco(self) -> int:
        """Extrai o preço do produto a partir do HTML.

        Args:
            html (str): O HTML do produto.

        Returns:
            int: O preço do produto.
        """
        price_element = self._doc.xpath(
            "//div[contains(@class,'payment-method-text')]"
            "[.//span[contains(@class,'payment-method-name') and "
            "normalize-space()='Cartão de Crédito']]"
            "//span[contains(@class,'payment-method-value')]/text()"
        )

        if price_element:
            return norm.normalizar_int(price_element[0])

        raise ValueError("Preço não encontrado")
