# flake8: noqa: E501

from pathlib import Path
from app.scrapping.product_parser import ProdutoParser

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def ler_html(arquivo: str) -> str:
    return (FIXTURES_DIR / arquivo).read_text(encoding="utf-8")


def test_parser_produto_1():
    html = ler_html("ventilador_item1.html")
    parser = ProdutoParser(html)

    produto = parser.parse_produto()

    assert produto.sku == 920183746512509
    assert produto.titulo == "Ventilador de Parede Oscilante 60cm 200W Light Maeto - Preto"
    assert produto.preco == 30513
    assert produto.preco_pix == 29292
    assert produto.valor_parcela == 3762
    assert produto.numero_parcela == 10
    assert produto.informacoes_tecnicas == {
        "Ajuste": "Inclinação + velocidade com controle deslizante",
        "Cor": "Preto",
        "Eficiência Energética": "Classe A",
        "Garantia": "1 ano",
        "Marca": "Maeto",
        "Medidas": "60X47X60cm",
        "Modelo": "Light – Oscilante de Parede",
        "Oscilação": "Automática",
        "Peso": "2,38 kg",
        "Potência (Watts)": "200W",
        "Quantidade de pás": "3 pás (design aerodinâmico)",
        "Rotação Máxima": "Até 1500 RPM",
        "Tensão": "Opções 127V, 220V ou Bivolt (selecionável)",
        "Tipo de Instalação": "Ventilador de parede (acompanha kit de fixação)",
    }


def test_parser_produto_2_desconto():
    html = ler_html("ventilador_item2_desconto.html")
    parser = ProdutoParser(html)

    produto = parser.parse_produto()

    assert produto.disponivel is True
    assert produto.sku == 920183746512503
    assert produto.titulo == "KIt 10 Assentos Carrara Soft Close - Maeto"
    assert produto.preco == 87410
    assert produto.preco_pix == 83914
    assert produto.valor_parcela == 10777
    assert produto.numero_parcela == 10
    assert produto.informacoes_tecnicas == {
        "Marca": "Maeto",
        "Cor": "Branco",
        "Formato anatômico": "U (aberto na frente)",
        "Material": "Polipropileno (PP) de alta resistência",
        "Acabamento": "Premium (visual sofisticado)",
        "Sistema de Limpeza": "Easy Clean (remoção rápida para higienização)",
        "Fixação": "Firme, segura e de instalação simples/intuitiva",
        "Embalagem": "Enviado em caixa (melhor proteção no transporte)",
        "Compatibilidade": "Deca: LK, Duna, Carrara, Nuova, Vogue Plus Roca: Nexo Celite: Smart Icasa: Vesuvio",
        "Indicação de uso": "reformas, obras, construtoras, hotéis e padronização de banheiros",
        "Garantia": "1 ano",
        "Disponibilidade": "Envio imediato (conforme estoque)",
    }


def test_parser_produto_3_indisponivel():
    html = ler_html("ventilador_item3_indisponivel.html")
    parser = ProdutoParser(html)

    produto = parser.parse_produto()

    assert produto.disponivel is False
    assert produto.sku == 337898940756104
    assert produto.titulo == "Circulador de Ar 35cm Potente Ventilador de Mesa Maeto - Preto/Bronze"
    assert produto.preco is None
    assert produto.preco_pix is None
    assert produto.valor_parcela is None
    assert produto.numero_parcela is None
    assert produto.informacoes_tecnicas == {
        "Cor": "Preto com detalhes em bronze",
        "Garantia": "12 meses",
        "Grade frontal": "35 cm",
        "Modelo": "Circulador de Ar Turbo 35cm – 45W",
        "Potência (Watts)": "45",
        "Tensão": "127 V ou 220 V",
        "Velocidades": "2 opções",
    }
