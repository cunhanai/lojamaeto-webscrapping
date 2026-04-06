from typing import Dict, Optional

from bs4 import BeautifulSoup
from app.domain.produto import Produto
from lxml import html
from lxml.etree import _Element
import app.scrapping.normalizers as norm


class ProdutoParser:
    _soup_base: BeautifulSoup
    _soup_detalhes: BeautifulSoup
    _doc: _Element

    def __init__(self, html_text: str):
        self._soup_base = BeautifulSoup(html_text, "lxml")

        detalhes = self._soup_base.select_one("#right-column")
        self._soup_detalhes = BeautifulSoup(str(detalhes), "lxml")

        self._doc = html.fromstring(html_text)

    def parse(self) -> Produto:
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
            preco_pix=self._extract_preco_pix(),
            valor_parcela=self._extract_valor_parcela(),
            numero_parcela=self._extract_numero_parcela(),
            informacoes_tecnicas=self._extract_informacoes_tecnicas(),
        )

    def _extract_sku(self) -> int:
        """Extrai o SKU do produto a partir do HTML.

        Args:
            html (str): O HTML do produto.

        Returns:
            int: O SKU do produto.
        """
        sku = self._soup_detalhes.select_one(".sku-active")

        if sku:
            return norm.converter_int(sku.text)

        raise ValueError("SKU não encontrado")

    def _extract_titulo(self) -> str:
        """Extrai o título do produto a partir do HTML.

        Args:
            html (str): O HTML do produto.

        Returns:
            str: O título do produto.
        """
        titulo = self._doc.xpath("//h1/span/text()")

        if titulo:
            return norm.normalizar_whitespaces(titulo[0])

        raise ValueError("Título não encontrado")

    def _extract_preco(self) -> Optional[int]:
        """Extrai o preço do produto a partir do HTML.

        Args:
            html (str): O HTML do produto.

        Returns:
            int: O preço do produto.
        """
        preco = self._doc.xpath(
            "//div[contains(@class,'payment-method-text')]"
            "[.//span[contains(@class,'payment-method-name') and "
            "normalize-space()='Cartão de Crédito']]"
            "//span[contains(@class,'payment-method-value')]/text()"
        )

        if preco:
            return norm.normalizar_int(preco[0])

        return None

    def _extract_preco_pix(self) -> Optional[int]:
        """Extrai o preço do produto para pagamento via Pix a partir do HTML.

        Args:
            html (str): O HTML do produto.

        Returns:
            int: O preço do produto para pagamento via Pix.
        """
        preco_pix = self._doc.xpath(
            "//div[contains(@class,'payment-method-text')]"
            "[.//span[contains(@class,'payment-method-name') and "
            "normalize-space()='Pix']]"
            "//span[contains(@class,'payment-method-value')]/text()"
        )

        if preco_pix:
            return norm.normalizar_int(preco_pix[0])

        return None

    def _extract_valor_parcela(self) -> Optional[int]:
        """Extrai o valor da parcela do produto a partir do HTML.

        Args:
            html (str): O HTML do produto.

        Returns:
            int: O valor da parcela do produto.
        """
        valor_parcela = self._soup_detalhes.select_one(".installments-amount")

        if valor_parcela:
            return norm.normalizar_int(valor_parcela.text)

        return None

    def _extract_numero_parcela(self) -> Optional[int]:
        """Extrai o número de parcelas do produto a partir do HTML.

        Args:
            html (str): O HTML do produto.

        Returns:
            int: O número de parcelas do produto.
        """
        numero_parcela = self._soup_detalhes.select_one(".installments-number")

        if numero_parcela:
            return norm.normalizar_int(numero_parcela.text)

        return None

    def _extract_informacoes_tecnicas(self) -> Dict[str, str]:
        """Extrai as informações técnicas do produto a partir do HTML.

        Args:
            html (str): O HTML do produto.

        Returns:
            Dict[str, str]: Um dicionário contendo as informações técnicas do
            produto.
        """
        informacoes_tecnicas = {}
        rows = self._soup_base.select(
            """#product-description-table-attributes
                                      tr"""
        )

        for row in rows:
            cols = row.select("td")

            chave = norm.normalizar_whitespaces(cols[0].text)
            valor = norm.normalizar_whitespaces(cols[1].text)
            informacoes_tecnicas[chave] = valor

        return informacoes_tecnicas
