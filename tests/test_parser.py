# flake8: noqa: E501

from pathlib import Path
from app.scrapping.product_parser import ProdutoParser

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def ler_html(arquivo: str) -> str:
    return (FIXTURES_DIR / arquivo).read_text(encoding="utf-8")


def test_parser_produto():
    html = ler_html("ventilador_item1.html")

    parser = ProdutoParser(html)
    produto = parser.parse_produto()

    assert produto.sku == 920183746512509
    assert produto.titulo == "Ventilador de Parede Oscilante 60cm 200W Light Maeto - Preto"
    assert produto.preco == 30513
    # assert produto.preco_pix == 29292
    # assert produto.valor_parcela == 3762
    # assert produto.numero_parcela == 10
