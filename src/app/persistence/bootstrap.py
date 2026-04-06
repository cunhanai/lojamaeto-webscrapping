from pathlib import Path
import importlib

from app.config import config
from app.persistence.database import Base, engine


def create_database() -> None:
    importlib.import_module("app.persistence.models.produto_orm")
    importlib.import_module("app.persistence.models.info_tecnica_orm")

    Path(config.db_path).parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
