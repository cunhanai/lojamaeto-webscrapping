from app.persistence.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import Integer, String, DateTime

from app.persistence.models.info_tecnica_orm import InformacaoTecnicaORM


class ProdutoORM(Base):
    __tablename__ = "produto"

    sku: Mapped[str] = mapped_column(String(50), primary_key=True)
    titulo: Mapped[str] = mapped_column(String(500), nullable=False)
    preco: Mapped[int | None] = mapped_column(Integer, nullable=True)
    preco_pix: Mapped[int | None] = mapped_column(Integer, nullable=True)
    valor_parcela: Mapped[int | None] = mapped_column(Integer, nullable=True)
    numero_parcela: Mapped[int | None] = mapped_column(Integer, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    informacoes_tecnicas: Mapped[list["InformacaoTecnicaORM"]] = relationship(
        back_populates="produto",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
