import time

def test_server_starts_fast():
    start = time.time()
    time.sleep(0.5)  # simulation d’un traitement léger
    duration = time.time() - start
    assert duration < 1, f"⚠️ Le test est trop lent : {duration:.2f}s"
