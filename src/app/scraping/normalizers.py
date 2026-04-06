import re


def normalizar_whitespaces(texto: str) -> str:
    """
    Remove espaços extras e normaliza os espaços em branco desnecessários.

    Args:
        texto (str): O texto a ser normalizado.

    returns:
        str: O texto normalizado, com espaços extras removidos.
    """
    return re.sub(r"\s+", " ", texto).strip()


def normalizar_int(texto: str) -> int:
    """Normaliza textos que representam valores monetários ou interios,
    removendo caracteres não numéricos e convertendo para inteiro.

    Args:
        texto (str): Valor no formato 'R$ 1.234,56', '134,56' ou '10x'

    Returns:
        int: O valor normalizado como um inteiro.
    """
    return int(re.sub(r"[^\d]", "", texto))
