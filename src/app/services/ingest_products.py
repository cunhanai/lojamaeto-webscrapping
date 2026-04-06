from app.scraping.client import MaetoClient
from app.scraping.parsers.product_parser import ProdutoParser
from app.scraping.parsers.search_result_parser import SearchResultParser


def run_ingestion(query: str, client: MaetoClient) -> list:
    html_busca = client.get("/search/", params={"q": query})
    links = SearchResultParser(html_busca).parse()

    produtos = []
    for link in links:
        html_produto = client.get(link)
        produto = ProdutoParser(html_produto).parse()
        produtos.append(produto)

    return produtos
