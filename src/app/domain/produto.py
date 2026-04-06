from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from app.domain.info_tecnica import InformacaoTecnica


class Produto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sku: str
    titulo: str
    preco: Optional[int] = None
    preco_pix: Optional[int] = None
    valor_parcela: Optional[int] = None
    numero_parcela: Optional[int] = None
    informacoes_tecnicas: List[InformacaoTecnica] = []
    disponivel: bool
