import pytest
from pokemon import Pokemon

def test_criar_pokemon():
    pikachu = Pokemon("Pikachu", "Eletrico")
    assert pikachu.nome == "Pikachu"
    assert pikachu.tipo == "Eletrico"
    assert pikachu.nivel == 1