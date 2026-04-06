from pathlib import Path

from app.config import config
from app.logger import setup_logger
from app.persistence.database import Base, engine

import app.persistence.models  # noqa: F401


def create_database() -> None:
    Path(config.db_path).parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)


def main() -> None:
    setup_logger(config.log_level)
    create_database()
    print(f"[OK] Banco criado/verificado em: {config.db_path}")


if __name__ == "__main__":
    main()
