from sqlalchemy import ForeignKey, UniqueConstraint, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.persistence.models.produto_orm import ProdutoORM
from app.persistence.database import Base


class InformacaoTecnicaORM(Base):
    __tablename__ = "produto_informacao_tecnica"
    __table_args__ = (
        UniqueConstraint(
            "product_sku",
            "nome",
            name="uq_produto_informacao_tecnica_nome",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    produto_sku: Mapped[str] = mapped_column(
        ForeignKey("produto.sku", ondelete="CASCADE"), nullable=False
    )
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    valor: Mapped[str] = mapped_column(Text, nullable=False)

    produto: Mapped["ProdutoORM"] = relationship(
        back_populates="informacoes_tecnicas",
    )
