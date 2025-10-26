import pytest
import sys
import os
sys.path.append(os.path.abspath('..'))

def loadCompetitions():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(BASE_DIR, 'competitions.json')) as comps:
        competitions = json.load(comps)['competitions']
    return competitions

def loadClubs():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, 'clubs.json')
    with open(file_path) as c:
        listOfClubs = json.load(c)['clubs']
    return listOfClubs

from server import app

@pytest.fixture
def client():
    """Client de test Flask réutilisable pour tous les tests."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.mark.parametrize("email,password,expected", [
    ('admin@admin.com', 'admin', 200),  # ✅ correct
    ('admin@imie-paris.fr', 'wrong', 403),  # ❌ mauvais mot de passe
    ('wrong@imie-paris.fr', 'admin', 403),  # ❌ mauvais email
    ('wrong@imie-paris.fr', 'wrong', 403)   # ❌ tout faux
])
def test_login_param(client, email, password, expected):
    response = client.post('/admin',  # ✅ c’est la bonne route de login
        data={'email': email, 'password': password},
        follow_redirects=True)
    assert response.status_code == expected
