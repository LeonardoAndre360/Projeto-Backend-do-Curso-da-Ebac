import pytest

def soma(a,b):
    return a * b

def test_soma_dois_numeros():
    resultado = soma(2,3)
    assert resultado == 6
    print(f"Resultado é igual a: {resultado}")

print(f"{test_soma_dois_numeros()}")