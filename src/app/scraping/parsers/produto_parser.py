from typing import List, Optional

from bs4 import BeautifulSoup
from lxml import html
from lxml.etree import _Element

from app.domain.info_tecnica import InformacaoTecnica
import app.scraping.normalizers as norm
from app.domain.produto import Produto


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
            sku=self._extrair_sku(),
            titulo=self._extrair_titulo(),
            preco=self._extrair_preco(),
            preco_pix=self._extrair_preco_pix(),
            valor_parcela=self._extrair_valor_parcela(),
            numero_parcela=self._extrair_numero_parcela(),
            informacoes_tecnicas=self._extrair_informacoes_tecnicas(),
            disponivel=self._extrair_preco() is not None,
        )

    def _extrair_sku(self) -> str:
        """Extrai o SKU do produto a partir do HTML.

        Args:
            html (str): O HTML do produto.

        Returns:
            str: O SKU do produto.
        """
        sku = self._soup_detalhes.select_one(".sku-active")

        if sku:
            return norm.normalizar_whitespaces(sku.text)

        raise ValueError("SKU não encontrado")

    def _extrair_titulo(self) -> str:
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

    def _extrair_preco(self) -> Optional[int]:
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

    def _extrair_preco_pix(self) -> Optional[int]:
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

    def _extrair_valor_parcela(self) -> Optional[int]:
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

    def _extrair_numero_parcela(self) -> Optional[int]:
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

    def _extrair_informacoes_tecnicas(self) -> List[InformacaoTecnica]:
        """Extrai as informações técnicas do produto a partir do HTML.

        Args:
            html (str): O HTML do produto.

        Returns:
            List[InformacaoTecnica]: Uma lista de objetos contendo as
            informações técnicas do produto.
        """
        informacoes_tecnicas = []
        rows = self._soup_base.select(
            """#product-description-table-attributes
                                      tr"""
        )

        for row in rows:
            cols = row.select("td")

            info = InformacaoTecnica(
                nome=norm.normalizar_whitespaces(cols[0].text).lower(),
                valor=norm.normalizar_whitespaces(cols[1].text),
            )

            informacoes_tecnicas.append(info)

        return informacoes_tecnicas
