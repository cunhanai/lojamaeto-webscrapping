from sqlalchemy.dialects.sqlite import insert

from app.persistence.models.info_tecnica_orm import InformacaoTecnicaORM


class InformacaoTecnicaRepository:
    def __init__(self, session):
        self.session = session

    def upsert(self, data: dict) -> None:
        stmt = insert(InformacaoTecnicaORM).values(**data)
        stmt = stmt.on_conflict_do_update(
            index_elements=[
                InformacaoTecnicaORM.produto_sku,
                InformacaoTecnicaORM.nome,
            ],
            set_={
                "valor": stmt.excluded.valor,
            },
        )
        self.session.execute(stmt)
