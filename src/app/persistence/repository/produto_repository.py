from datetime import datetime
from sqlalchemy.dialects.sqlite import insert

from app.persistence.models.produto_orm import ProdutoORM


class ProdutoRepository:
    def __init__(self, session):
        self.session = session

    def upsert(self, data: dict) -> None:
        now = datetime.now()
        stmt = insert(ProdutoORM).values(
            **data,
            criado_em=now,
            atualizado_em=now,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[ProdutoORM.sku],
            set_={
                "titulo": stmt.excluded.titulo,
                "preco": stmt.excluded.preco,
                "preco_pix": stmt.excluded.preco_pix,
                "valor_parcela": stmt.excluded.valor_parcela,
                "numero_parcela": stmt.excluded.numero_parcela,
                "criado_em": stmt.excluded.criado_em,
                "atualizado_em": stmt.excluded.atualizado_em,
            },
        )
        self.session.execute(stmt)
