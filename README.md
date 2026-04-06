# Loja Maeto Web Scrapping

Projeto de scraping para consultar produtos da Loja Maeto com banco SQLite.

## Objetivo

O objetivo desta aplicação é:

- Buscar produtos por termo de pesquisa no site da Loja Maeto
- Extrair dados principais do produto e suas informações técnicas
- Atualizar os dados no banco a cada nova execução
- Apresentar um resumo das informações pesquisadas ao usuário

## Tecnologias

- Python 3.12+
- Typer (CLI)
- HTTPX (cliente HTTP)
- BeautifulSoup + lxml (parsing)
- SQLAlchemy (persistencia)
- SQLite (banco local)
- Pytest (testes)

## Estrutura do Banco

O banco fica em:

- `./data/maeto.db`

Tabelas:

- `produto`
- `produto_informacao_tecnica`

## Como criar o banco

Por padrao, ao executar o comando do projeto com `run`, o banco e criado/verificado automaticamente (flag `--init-db` vem ligada).

- `scraper run -q "ventilador" --no-init-db`

## Passo a passo para executar

## 1) Criar variáveis de ambiente

No repositório está salvo o arquivo `.env.example` que contém os padrões das variáveis de ambiente que utilizei.

Você pode copiar o conteúdo desse arquivo para o `.env` ou criar um novo alterando as informações caso necessário.

Variáveis de ambiente padrões:

```text
APP_ENV=dev
LOG_LEVEL=INFO
DB_PATH=./data/maeto.db
HTTP_TIMEOUT=20
USER_AGENT=Mozilla/5.0 (compatible; LojaMaetoWebscraper/1.0)
BASE_URL=https://www.lojamaeto.com
```

As principais variáveis são:

- **DB_PATH:** Caminho onde o banco de dados será criado e salvo
- **BASE_URL:** URL base da Loja Maeto para scraping dos produtos.

## 2) Criar e ativar ambiente virtual

Na pasta do projeto, crie e ative o ambiente virtual.

Exemplo no Windows PowerShell:

```shell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3) Instalar dependencias

```shell
pip install -e .
```

Para ambiente de desenvolvimento (testes, lint, etc.):

```shell
pip install -e .[dev]
```

## 4) Executar uma pesquisa

Exemplo:

```powershell
scraper run -q "sua pesquisa"
```

A saida no CLI mostra apenas os produtos da consulta atual, em formato legivel, com bloco de informacoes tecnicas embaixo de cada produto.

## 5) Rodar testes unitários

Após instalar as dependências para ambiente de desenvolvimento, rode:

```powershell
pytest -q
```

## Comandos uteis

- Ver ajuda do comando de pesquisa:

```powershell
scraper run --help
```

- Pesquisa com inicialização automática do banco:

```powershell
scraper run -q "ventilador"
```

- Pesquisa sem inicializar banco:

```powershell
scraper run -q "ventilador" --no-init-db
```

## Observações

- O projeto faz upsert: se o SKU já existir, os dados do produto e das informacoes tecnicas são atualizados.

- O banco SQLite pode ser aberto por extensoes de visualizacao SQL, como o `SQLite Viewer` para Visual Studio Code

- Por padrão, o banco de dados é salvo em `./data/maeto.db`, mas você pode alterar sobrescrevedo a variável de embiente `DB_PATH` em `.env`
