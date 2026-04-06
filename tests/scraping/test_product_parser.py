# flake8: noqa: E501

from pathlib import Path
from app.scraping.parsers.product_parser import ProdutoParser

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def ler_html(arquivo: str) -> str:
    return (FIXTURES_DIR / arquivo).read_text(encoding="utf-8")


def test_parser_produto_1():
    html = ler_html("ventilador_item1.html")
    parser = ProdutoParser(html)

    produto = parser.parse()

    assert produto.disponivel is True
    assert produto.sku == "920183746512509"
    assert produto.titulo == "Ventilador de Parede Oscilante 60cm 200W Light Maeto - Preto"
    assert produto.preco == 30513
    assert produto.preco_pix == 29292
    assert produto.valor_parcela == 3762
    assert produto.numero_parcela == 10
    assert len(produto.informacoes_tecnicas) == 14


def test_parser_produto_2_desconto():
    html = ler_html("ventilador_item2_desconto.html")
    parser = ProdutoParser(html)

    produto = parser.parse()

    assert produto.disponivel is True
    assert produto.sku == "920183746512503"
    assert produto.titulo == "KIt 10 Assentos Carrara Soft Close - Maeto"
    assert produto.preco == 87410
    assert produto.preco_pix == 83914
    assert produto.valor_parcela == 10777
    assert produto.numero_parcela == 10
    assert len(produto.informacoes_tecnicas) == 12


def test_parser_produto_3_indisponivel():
    html = ler_html("ventilador_item3_indisponivel.html")
    parser = ProdutoParser(html)

    produto = parser.parse()

    assert produto.disponivel is False
    assert produto.sku == "337898940756104"
    assert produto.titulo == "Circulador de Ar 35cm Potente Ventilador de Mesa Maeto - Preto/Bronze"
    assert produto.preco is None
    assert produto.preco_pix is None
    assert produto.valor_parcela is None
    assert produto.numero_parcela is None
    assert len(produto.informacoes_tecnicas) == 7
