from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Produto:
    sku: int
    titulo: str
    preco: float
    preco_pix: float
    valor_parcela: float
    numero_parcela: int
    informacoes_tecnicas: Dict[str, Any] = field(default_factory=dict)

    def __init__(
        self,
        sku: int,
        titulo: str,
        preco: float,
        # preco_pix: float,
        # valor_parcela: float,
        # numero_parcela: int,
        # informacoes_tecnicas: Dict[str, Any] = field(default_factory=dict),
    ):
        self.sku = sku
        self.titulo = titulo
        self.preco = preco
        # self.preco_pix = preco_pix
        # self.valor_parcela = valor_parcela
        # self.numero_parcela = numero_parcela
        # self.informacoes_tecnicas = informacoes_tecnicas

    def __repr__(self):
        return f"""Produto(sku={self.sku!r},
                    titulo={self.titulo!r},
                    preco={self.preco!r},
                    preco_pix={self.preco_pix!r},
                    valor_parcela={self.valor_parcela!r},
                    numero_parcela={self.numero_parcela!r},
                    informacoes_tecnicas={self.informacoes_tecnicas!r})
                """
