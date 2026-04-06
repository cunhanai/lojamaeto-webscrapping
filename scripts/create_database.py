from app.config import config
from app.logger import setup_logger
from app.persistence.bootstrap import create_database


def main() -> None:
    setup_logger(config.log_level)
    create_database()
    print(f"[OK] Banco criado/verificado em: {config.db_path}")


if __name__ == "__main__":
    main()
