import logging
import typer

from app.config import config
from app.logger import setup_logger
from scripts.create_database import create_database

app = typer.Typer(help="Loja Maeto scraper")


@app.command()
def run(
    query: str = typer.Option(..., "--query", "-q", help="Termo de busca"),
    init_db: bool = typer.Option(
        True, "--init-db/--no-init-db", help="Inicializa banco ao iniciar"
    ),
) -> None:
    setup_logger(config.log_level)
    logger = logging.getLogger(__name__)

    if init_db:
        create_database()
        logger.info("Banco inicializado/verificado.")

    # TODO: chamar seu serviço de ingestão
    logger.info("Iniciando scraping para query='%s'", query)
    logger.info("BASE_URL=%s", config.base_url)
    logger.info("Finalizado.")


if __name__ == "__main__":
    app()
