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

def test_home_page_returns_correct_html_naif(client):
    response = client.get('/')
    assert response.status_code == 200
    assert '<form' in response.get_data(as_text=True)


def test_home_page_accepts_post_request(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True)
    assert response.status_code == 200

