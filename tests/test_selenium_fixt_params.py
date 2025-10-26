import pytest
from selenium import webdriver

@pytest.fixture(params=["chrome", "firefox", "edge"])
def browser(request):
    """Fixture paramétrée pour lancer le même test sur plusieurs navigateurs."""
    driver = None
    if request.param == "chrome":
        driver = webdriver.Chrome()
    elif request.param == "firefox":
        driver = webdriver.Firefox()
    elif request.param == "edge":
        driver = webdriver.Edge()
    
    driver.maximize_window()
    yield driver
    driver.quit()

def test_home_page_loads_in_all_browsers(browser):
    """Vérifie que la page d'accueil s'affiche correctement sur tous les navigateurs."""
    browser.get("http://127.0.0.1:5000/")  # ton appli Flask doit tourner
    assert "Welcome" in browser.page_source or "Connexion" in browser.page_source
