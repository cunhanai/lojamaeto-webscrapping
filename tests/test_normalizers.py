# flake8: noqa: E501

import app.scrapping.normalizers as norm


def test_normalizar_whitespaces_titulo_1():
    texto = """
    
                    Ventilador de Parede Oscilante 60cm 
                    147W Light
                     Maeto - Preto
        
                            
    """
    resultado = norm.normalizar_whitespaces(texto)
    assert resultado == "Ventilador de Parede Oscilante 60cm 147W Light Maeto - Preto"


def test_normalizar_whitespaces_titulo_2():
    texto = """
                    Circulador de Ar 35cm Potente Ventilador de Mesa Maeto - Preto/Bronze
        
                            """
    resultado = norm.normalizar_whitespaces(texto)
    assert resultado == "Circulador de Ar 35cm Potente Ventilador de Mesa Maeto - Preto/Bronze"


def test_normalizar_int_preco_1():
    texto = "R$ 1.234,56"
    resultado = norm.normalizar_int(texto)
    assert resultado == 123456


def test_normalizar_int_preco_2():
    texto = "134,56"
    resultado = norm.normalizar_int(texto)
    assert resultado == 13456


def test_normalizar_int_parcela():
    texto = "10x"
    resultado = norm.normalizar_int(texto)
    assert resultado == 10


def test_converter_int():
    texto = "10"
    resultado = norm.converter_int(texto)
    assert resultado == 10
