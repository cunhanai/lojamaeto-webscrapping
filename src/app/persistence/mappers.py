from app.domain.produto import Produto
from app.domain.info_tecnica import InformacaoTecnica
from app.persistence.models.produto_orm import ProdutoORM


def domain_to_orm(produto: Produto) -> tuple[dict, list[dict]]:
    product_data = {
        "sku": produto.sku,
        "title": produto.titulo,
        "price_cents": produto.preco,
        "pix_price_cents": produto.preco_pix,
        "installment_value_cents": produto.valor_parcela,
        "installment_count": produto.numero_parcela,
        "source_url": None,
    }

    specs_data = [
        {
            "product_sku": produto.sku,
            "spec_key": info.nome.strip().lower(),
            "spec_value": info.valor.strip(),
        }
        for info in produto.informacoes_tecnicas
    ]
    return product_data, specs_data


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
