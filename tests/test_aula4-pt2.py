import pytest

def test_ganhar_xp_sobe_nivel():
    bulbasaur = Pokemon("Bulbasaur", "Planta")
    bulbasaur.ganhar_xp(120)
    assert bulbasaur.nivel == 2
    assert bulbasaur.xp == 20

class Pokemon:
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo
        self.nivel = 1
        self.xp = 0

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        while self.xp >= 100:
            self.nivel += 1
            self.xp -= 100