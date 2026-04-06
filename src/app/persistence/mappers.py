from app.domain.produto import Produto
from app.domain.info_tecnica import InformacaoTecnica
from app.persistence.models.produto_orm import ProdutoORM


def domain_to_orm(produto: Produto) -> tuple[dict, list[dict]]:
    dados_produto = {
        "sku": produto.sku,
        "titulo": produto.titulo,
        "preco": produto.preco,
        "preco_pix": produto.preco_pix,
        "valor_parcela": produto.valor_parcela,
        "numero_parcela": produto.numero_parcela,
    }

    dados_info_tecnica = [
        {
            "produto_sku": produto.sku,
            "nome": info.nome.strip().lower(),
            "valor": info.valor.strip(),
        }
        for info in produto.informacoes_tecnicas
    ]
    return dados_produto, dados_info_tecnica


def orm_to_domain(produto_orm: ProdutoORM) -> Produto:
    infos = [
        InformacaoTecnica(nome=spec.nome, valor=spec.valor)
        for spec in produto_orm.informacoes_tecnicas
    ]

    return Produto(
        sku=produto_orm.sku,
        titulo=produto_orm.titulo,
        preco=produto_orm.preco,
        preco_pix=produto_orm.preco_pix,
        valor_parcela=produto_orm.valor_parcela,
        numero_parcela=produto_orm.numero_parcela,
        informacoes_tecnicas=infos,
        disponivel=True,
    )
