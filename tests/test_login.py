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
    """
    Fixture qui crée un client de test Flask.
    Ce client simule un navigateur web pour interagir avec l’application
    sans la lancer réellement dans un serveur externe.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_admin_login_denied_with_wrong_credentials(client):
    resp = client.post("/admin",
                       data={"email": "wrong", "password": "wrong"},
                       follow_redirects=True)
    # Le serveur renvoie 403 en cas d’échec
    assert resp.status_code == 403
    page = resp.get_data(as_text=True).lower()
    # on voit la page de connexion (titre + formulaire)
    assert "welcome to the admin portal" in page
    assert '<form action="/admin" method="post">' in page
    # on NE voit PAS la page admin
    assert "welcome admin" not in page and "admin.html" not in page

@pytest.mark.parametrize("email,password,expected", [
    ('admin@admin.com', 'admin', 200),   # ✅ succès
    ('admin@admin.com', 'wrong', 403),  # ❌ mauvais mdp
    ('wrong@imie-paris.fr', 'admin', 403),  # ❌ mauvais email
    ('wrong@imie-paris.fr', 'wrong', 403),  # ❌ tout faux
])
def test_login_param(client, email, password, expected):
    resp = client.post(
        '/admin',  # IMPORTANT: poster sur /admin, pas /ConnexionAdmin
        data={'email': email, 'password': password},
        follow_redirects=True
    )
    assert resp.status_code == expected