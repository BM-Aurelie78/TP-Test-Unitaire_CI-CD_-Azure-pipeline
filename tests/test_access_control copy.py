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


def test_cannot_access_welcome_without_input(client):
    """
    3.6 : Vérifie qu'on ne peut pas accéder à la page 'welcome' sans saisir de texte ou d'email.
    """
    response = client.post('/showSummary', data={'email': ''}, follow_redirects=False)
    # L'accès doit être refusé (redirection ou erreur)
    assert response.status_code in (302, 403, 400), "❌ La page welcome est accessible sans saisie !"


def test_cannot_access_admin_directly(client):
    """
    3.6 : Vérifie qu'on ne peut pas accéder directement à la page admin sans login.
    """
    response = client.get('/admin', follow_redirects=True)
    assert response.status_code in (302, 403, 401), "❌ L'admin page est accessible sans authentification !"
