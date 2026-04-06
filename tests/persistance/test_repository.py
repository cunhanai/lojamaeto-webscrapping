from pathlib import Path

from sqlalchemy import text

from app.persistence.database import engine, Base
import app.persistence.models  # noqa: F401


def test_conexao_engine():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar_one()
        assert result == 1


def test_criar_banco_dados(tmp_path):
    db_file = tmp_path / "test_products.db"
    test_url = f"sqlite:///{db_file}"

    from sqlalchemy import create_engine

    test_engine = create_engine(test_url, future=True)

    Base.metadata.create_all(bind=test_engine)

    assert Path(db_file).exists()
