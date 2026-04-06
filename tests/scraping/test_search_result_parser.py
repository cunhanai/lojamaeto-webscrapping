# flake8: noqa: E501

from pathlib import Path
from app.scraping.parsers.search_parser import SearchResultParser

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def ler_html(arquivo: str) -> str:
    return (FIXTURES_DIR / arquivo).read_text(encoding="utf-8")


def test_parse():
    html = ler_html("ventilador_lista.html")
    parser = SearchResultParser(html)

    rows = parser.parse()

    assert len(rows) == 14
    assert rows[0] == "/ventilador-osc-de-coluna-40-cm-126w-turbo-preto-ventimais"
    assert rows[1] == "/ventilador-osc-de-parede-60-cm-light-147w-maeto"
    assert rows[2] == "/ventilador-mini-turbo-20cm-preto-prata-ventimais"
    assert rows[3] == "/ventilador-mini-turbo-20cm-branco-prata-ventimais"
    assert rows[4] == "/ventilador-de-teto-firenze-com-led-branco"
    assert rows[5] == "/ventilador-de-teto-firenze-sem-led-preto"
    assert rows[6] == "/ventilador-de-teto-firenze-sem-led-branco"
    assert rows[7] == "/ventilador-osc-de-parede-60-cm-light-200w-maeto"
    assert rows[8] == "/ventilador-de-teto-firenze-com-led-preto"
    assert rows[9] == "/ventilador-de-teto-firenze-com-led-com-controle-remoto-preto"
    assert rows[10] == "/ventilador-osc-mesa-30cm-55w-turbo-ventimais-preto"
    assert rows[11] == "/ventilador-de-teto-firenze-com-led-com-controle-remoto-branco"
    assert rows[12] == "/circulador-de-ar-25cm-ventimais"
    assert rows[13] == "/circulador-de-ar-35cm-preto-bronze-ventimais"
