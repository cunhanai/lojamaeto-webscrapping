import logging
from sqlalchemy import select

from app.domain.produto import Produto
from app.persistence.database import SessionLocal
from app.persistence.models.produto_orm import ProdutoORM
from app.persistence.repository.info_tecnica_repository import (
    InformacaoTecnicaRepository,
)
from app.persistence.repository.produto_repository import ProdutoRepository
from app.scraping.client import MaetoClient
from app.scraping.parsers.produto_parser import ProdutoParser
from app.scraping.parsers.search_parser import SearchResultParser


logger = logging.getLogger(__name__)


def run_ingestion(query: str, client: MaetoClient) -> list[Produto]:
    logger.info("Buscando links de produtos para query='%s'", query)
    html_busca = client.get("/search/", params={"q": query})
    links = SearchResultParser(html_busca).parse()
    logger.info("Total de links encontrados: %s", len(links))

    produtos: list[Produto] = []

    for link in links:
        html_produto = client.get(link)
        produto = ProdutoParser(html_produto).parse()
        produtos.append(produto)

    logger.info("Total de produtos parseados: %s", len(produtos))

    return produtos


def salvar_produtos(produtos: list[Produto]) -> int:
    with SessionLocal() as session:
        produto_repository = ProdutoRepository(session)
        info_tecnica_repository = InformacaoTecnicaRepository(session)

        for produto in produtos:
            produto_repository.upsert(
                {
                    "sku": produto.sku,
                    "titulo": produto.titulo,
                    "preco": produto.preco,
                    "preco_pix": produto.preco_pix,
                    "valor_parcela": produto.valor_parcela,
                    "numero_parcela": produto.numero_parcela,
                }
            )

            for info_tecnica in produto.informacoes_tecnicas:
                info_tecnica_repository.upsert(
                    {
                        "produto_sku": produto.sku,
                        "nome": info_tecnica.nome.strip().lower(),
                        "valor": info_tecnica.valor.strip(),
                    }
                )

        session.commit()

    logger.info("Total de produtos salvos/atualizados: %s", len(produtos))
    return len(produtos)


def listar_produtos_por_skus(skus: list[str]) -> list[ProdutoORM]:
    if not skus:
        return []

    skus_unicos = list(dict.fromkeys(skus))

    with SessionLocal() as session:
        stmt = (
            select(ProdutoORM)
            .where(ProdutoORM.sku.in_(skus_unicos))
            .order_by(ProdutoORM.titulo.asc())
        )
        produtos_banco = list(session.execute(stmt).scalars().all())

    logger.info(
        "Total de produtos retornados para a consulta atual: %s",
        len(produtos_banco),
    )
    return produtos_banco


def run_ingestion_and_save(
    query: str,
    client: MaetoClient,
) -> tuple[int, list[ProdutoORM]]:
    produtos = run_ingestion(query=query, client=client)
    salvos = salvar_produtos(produtos)
    skus_consulta = [produto.sku for produto in produtos]
    produtos_banco = listar_produtos_por_skus(skus_consulta)
    return salvos, produtos_banco


def executar_ingest(
    query: str,
    *,
    base_url: str,
    timeout: int,
    user_agent: str,
) -> tuple[int, list[ProdutoORM]]:
    logger.info("Iniciando scraping para query='%s'", query)
    logger.info("BASE_URL=%s", base_url)

    client = MaetoClient(
        base_url=base_url,
        timeout=timeout,
        user_agent=user_agent,
    )

    try:
        return run_ingestion_and_save(query=query, client=client)
    finally:
        client.close()


def montar_resumo_cli(
    query: str,
    total_salvos: int,
    produtos_banco: list[ProdutoORM],
) -> list[str]:
    linhas = [
        f"[OK] Consulta: {query}",
        f"[OK] Produtos processados e salvos: {total_salvos}",
        f"[OK] Produtos retornados desta consulta: {len(produtos_banco)}",
    ]

    if not produtos_banco:
        linhas.append("Nenhum produto encontrado para a consulta.")
        return linhas

    linhas.append("\nResultados da consulta:")

    for indice, produto in enumerate(produtos_banco, start=1):
        preco = (
            f"R$ {produto.preco / 100:.2f}".replace(".", ",")
            if produto.preco is not None
            else "sem preco"
        )

        preco_pix = (
            f"R$ {produto.preco_pix / 100:.2f}".replace(".", ",")
            if produto.preco_pix is not None
            else "sem preco"
        )

        parcela = "sem parcelamento"

        if produto.numero_parcela is not None and produto.valor_parcela is not None:
            valor_parcela = f"R$ {produto.valor_parcela / 100:.2f}".replace(".", ",")
            parcela = f"{produto.numero_parcela}x de {valor_parcela}"

        linhas.append("")
        linhas.append(f"[{indice}] {produto.titulo}")
        linhas.append(f"    SKU: {produto.sku}")
        linhas.append(f"    Preco: {preco}")
        linhas.append(f"    Preco pix: {preco_pix}")
        linhas.append(f"    Parcelamento: {parcela}")

        if not produto.informacoes_tecnicas:
            linhas.append("    Informacoes tecnicas: nao informado")
            continue

        linhas.append("    Informacoes tecnicas:")
        infos_ordenadas = sorted(
            produto.informacoes_tecnicas,
            key=lambda info: info.nome,
        )

        for info in infos_ordenadas:
            linhas.append(f"      - {info.nome}: {info.valor}")

    return linhas
