# Loja Maeto Web Scrapping

Projeto de scraping para consultar produtos da Loja Maeto, normalizar dados e persistir em banco SQLite.

## Objetivo

O objetivo desta aplicacao e:

- buscar produtos por termo de pesquisa no site da Loja Maeto;
- extrair dados principais do produto (sku, titulo, preco, preco pix e parcelamento);
- extrair e salvar informacoes tecnicas de cada produto;
- atualizar os dados no banco a cada nova execucao (upsert);
- apresentar no CLI somente os resultados da consulta atual, incluindo informacoes tecnicas carregadas do banco.

## Tecnologias

- Python 3.12+
- Typer (CLI)
- HTTPX (cliente HTTP)
- BeautifulSoup + lxml (parsing)
- SQLAlchemy (persistencia)
- SQLite (banco local)
- Pytest (testes)

## Estrutura do Banco

O banco padrao fica em:

- `./data/maeto.db`

Tabelas principais:

- `produto`
- `produto_informacao_tecnica`

## Como criar o banco

Nao precisa rodar migracao manual para iniciar.

Por padrao, ao executar o comando do projeto com `run`, o banco e criado/verificado automaticamente (flag `--init-db` vem ligada).

Opcoes:

1. Criacao automatica (recomendada):
   - execute `scraper run -q "ventilador"`
2. Criacao manual:
   - execute `python scripts/create_database.py`

Se quiser pular a inicializacao automatica (quando o banco ja existe), use:

- `scraper run -q "ventilador" --no-init-db`

## Passo a passo para executar

## 1) Criar e ativar ambiente virtual

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2) Instalar dependencias

```powershell
pip install -e .
```

Para ambiente de desenvolvimento (testes, lint etc):

```powershell
pip install -e .[dev]
```

## 3) Executar uma pesquisa

Exemplo:

```powershell
scraper run -q "lampada"
```

A saida no CLI mostra apenas os produtos da consulta atual, em formato legivel, com bloco de informacoes tecnicas embaixo de cada produto.

## 4) Rodar testes

```powershell
pytest -q
```

## Precisa compilar antes?

Nao.

Como e um projeto Python, basta instalar as dependencias e executar o comando CLI.

## Comandos uteis

- Ver ajuda geral:

```powershell
scraper --help
```

- Ver ajuda do comando de pesquisa:

```powershell
scraper run --help
```

- Pesquisa com inicializacao automatica do banco:

```powershell
scraper run -q "ventilador"
```

- Pesquisa sem inicializar banco:

```powershell
scraper run -q "ventilador" --no-init-db
```

## Observacoes

- O projeto faz upsert: se o SKU ja existir, os dados do produto e das informacoes tecnicas sao atualizados.
- O banco SQLite pode ser aberto por extensoes de visualizacao SQL; confirme que o arquivo aberto e `./data/maeto.db`.
