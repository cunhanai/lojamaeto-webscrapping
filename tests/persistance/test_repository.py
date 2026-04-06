from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy import select

from app.persistence.database import Base, engine
from app.persistence.models.info_tecnica_orm import InformacaoTecnicaORM
from app.persistence.models.produto_orm import ProdutoORM
import app.persistence.models.info_tecnica_orm  # noqa: F401
import app.persistence.models.produto_orm  # noqa: F401
from app.persistence.repository.info_tecnica_repository import (
    InformacaoTecnicaRepository,
)
from app.persistence.repository.produto_repository import ProdutoRepository


def test_conexao_engine():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar_one()
        assert result == 1


def test_criar_banco_dados(tmp_path):
    db_file = tmp_path / "test_products.db"
    test_url = f"sqlite:///{db_file}"

    test_engine = create_engine(test_url, future=True)

    Base.metadata.create_all(bind=test_engine)

    assert Path(db_file).exists()


def test_criar_tabelas_com_nomes_em_portugues(tmp_path):
    db_file = tmp_path / "schema_portugues.db"
    test_engine = create_engine(f"sqlite:///{db_file}", future=True)

    Base.metadata.create_all(bind=test_engine)

    inspetor = inspect(test_engine)
    tabelas = set(inspetor.get_table_names())

    assert "produto" in tabelas
    assert "produto_informacao_tecnica" in tabelas


def test_criar_colunas_produto_em_portugues(tmp_path):
    db_file = tmp_path / "schema_produto.db"
    test_engine = create_engine(f"sqlite:///{db_file}", future=True)

    Base.metadata.create_all(bind=test_engine)

    inspetor = inspect(test_engine)
    colunas = {coluna["name"] for coluna in inspetor.get_columns("produto")}

    assert {
        "sku",
        "titulo",
        "preco",
        "preco_pix",
        "valor_parcela",
        "numero_parcela",
        "criado_em",
        "atualizado_em",
    }.issubset(colunas)


def test_criar_colunas_info_tecnica_em_portugues(tmp_path):
    db_file = tmp_path / "schema_info.db"
    test_engine = create_engine(f"sqlite:///{db_file}", future=True)

    Base.metadata.create_all(bind=test_engine)

    inspetor = inspect(test_engine)
    colunas = {coluna["name"] for coluna in inspetor.get_columns("produto_informacao_tecnica")}

    assert {
        "id",
        "produto_sku",
        "nome",
        "valor",
    }.issubset(colunas)


def test_repository_upsert_persiste_produto(tmp_path):
    db_file = tmp_path / "persistencia.db"
    test_engine = create_engine(f"sqlite:///{db_file}", future=True)
    sessao_teste = sessionmaker(bind=test_engine, future=True)

    Base.metadata.create_all(bind=test_engine)

    with sessao_teste() as sessao:
        repositorio = ProdutoRepository(sessao)
        repositorio.upsert(
            {
                "sku": "sku-teste-001",
                "titulo": "Produto Teste",
                "preco": 12345,
                "preco_pix": 12000,
                "valor_parcela": 1234,
                "numero_parcela": 10,
            }
        )
        sessao.commit()

        produto = sessao.get(ProdutoORM, "sku-teste-001")
        assert produto is not None
        assert produto.titulo == "Produto Teste"


def test_repository_upsert_persiste_e_atualiza_info_tecnica(tmp_path):
    db_file = tmp_path / "persistencia_info.db"
    test_engine = create_engine(f"sqlite:///{db_file}", future=True)
    sessao_teste = sessionmaker(bind=test_engine, future=True)

    Base.metadata.create_all(bind=test_engine)

    with sessao_teste() as sessao:
        produto_repository = ProdutoRepository(sessao)
        info_repository = InformacaoTecnicaRepository(sessao)

        produto_repository.upsert(
            {
                "sku": "sku-teste-002",
                "titulo": "Produto Tecnico",
                "preco": 1000,
                "preco_pix": 950,
                "valor_parcela": 100,
                "numero_parcela": 10,
            }
        )

        info_repository.upsert(
            {
                "produto_sku": "sku-teste-002",
                "nome": "potencia",
                "valor": "126w",
            }
        )
        info_repository.upsert(
            {
                "produto_sku": "sku-teste-002",
                "nome": "potencia",
                "valor": "150w",
            }
        )
        sessao.commit()

        stmt = select(InformacaoTecnicaORM).where(
            InformacaoTecnicaORM.produto_sku == "sku-teste-002"
        )
        infos = list(sessao.execute(stmt).scalars().all())

        assert len(infos) == 1
        assert infos[0].nome == "potencia"
        assert infos[0].valor == "150w"
