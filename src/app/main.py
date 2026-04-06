import typer

from app.config import config
from app.logger import setup_logger
from app.persistence.bootstrap import create_database
from app.services import ingest_produtos

app = typer.Typer(help="Loja Maeto scraper")


@app.callback()
def cli() -> None:
    """CLI raiz do scraper."""


@app.command()
def run(
    query: str = typer.Option(..., "--query", "-q", help="Termo de busca"),
    init_db: bool = typer.Option(
        True, "--init-db/--no-init-db", help="Inicializa banco ao iniciar"
    ),
) -> None:
    setup_logger(config.log_level)

    if init_db:
        create_database()

    total_salvos, produtos_banco = ingest_produtos.executar_ingest(
        query=query,
        base_url=config.base_url,
        timeout=config.http_timeout,
        user_agent=config.user_agent,
    )

    linhas = ingest_produtos.montar_resumo_cli(
        query=query,
        total_salvos=total_salvos,
        produtos_banco=produtos_banco,
    )
    for linha in linhas:
        typer.echo(linha)


if __name__ == "__main__":
    app()
