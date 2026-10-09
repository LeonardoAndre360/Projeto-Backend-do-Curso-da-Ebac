import pytest

# Fixture para o pikachu
@pytest.fixture
def pikachu():
    return {"nome": "Pikachu", "tipo": "Elétrico", "nivel": 15}

# Fixture para o charmander
@pytest.fixture
def charmander():
    return {"nome": "Charmander", "tipo": "Fogo", "nivel": 12}

# Teste que utiliza ambas as fixtures
def test_pokemon_types(pikachu, charmander):
    assert pikachu["nivel"] > charmander["nivel"]