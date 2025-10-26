import os, time, socket, threading, pytest
from server import app

@pytest.fixture(scope="module")
def client():
    """Fixture Flask réutilisable pour tous les tests."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def wait_port(host="127.0.0.1", port=5000, timeout=10):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.2)
    return False

@pytest.fixture(scope="session", autouse=True)
def run_server_once():
    # Lancer Flask dans un thread (pas de reloader, pas de debug)
    def run():
        app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    # Attendre que le port soit ouvert
    assert wait_port(), "Le serveur Flask n'a pas démarré sur 127.0.0.1:5000"
    yield
    # rien à faire : thread daemon s’arrêtera à la fin des tests