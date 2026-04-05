from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Produto:
    sku: int
    titulo: str
    preco: Optional[int]
    preco_pix: Optional[int]
    valor_parcela: Optional[int]
    numero_parcela: Optional[int]
    informacoes_tecnicas: Dict[str, str]
    disponivel: bool

    def __init__(
        self,
        sku: int,
        titulo: str,
        preco: Optional[int],
        preco_pix: Optional[int],
        valor_parcela: Optional[int],
        numero_parcela: Optional[int],
        informacoes_tecnicas: Dict[str, str],
    ):
        self.sku = sku
        self.titulo = titulo
        self.preco = preco
        self.preco_pix = preco_pix
        self.valor_parcela = valor_parcela
        self.numero_parcela = numero_parcela
        self.informacoes_tecnicas = informacoes_tecnicas
        self.disponivel = self.preco is not None

    def __repr__(self):
        return f"""Produto(sku={self.sku!r},
                    titulo={self.titulo!r},
                    preco={self.preco!r},
                    preco_pix={self.preco_pix!r},
                    valor_parcela={self.valor_parcela!r},
                    numero_parcela={self.numero_parcela!r},
                    informacoes_tecnicas={self.informacoes_tecnicas!r})
                """
