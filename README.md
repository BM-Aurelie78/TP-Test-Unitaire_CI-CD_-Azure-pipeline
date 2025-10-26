# TP-Test-Unitaire_CI-CD_-Azure-pipeline

3.1)	La WebApp se lance correctement et la page Home s’affiche proprement ? 
Indice : status_code = 200, <form in response.data
test_route.py, se limiter au : test_home_page_returns_correct_html_naif


Lancement du programme test « test_home_page_returns_correct_html_naif » dans le fichier "test_route.py":
Pour cibler un test précis sans lancer toute la suite,pour déboguer un test qui échoue,avoir plus de détails sur ce que fait le test et pourquoi il échoue ou réussit.

pytest tests/test_route.py::test_home_page_returns_correct_html_naif -vv

Message dans le terminal de VS Code que la WebApp se lance et que la page Home répond avec succès (status_code 200)
------
3.2)	La page Home permet des requêtes POST valides (et que votre message personnalisé est affiché dans la page show Summary) ?
Indice : tester.post('/', data={"text":"sayf"}, follow_redirects=True)
test_route.py, se limiter au : test_home_page_accepts_post_request

Lancement du programme test “test_home_page_accepts_post_request” dans le fichier "test_route.py":

Pour cibler un test précis sans lancer toute la suite,pour déboguer un test qui échoue,avoir plus de détails sur ce que fait le test et pourquoi il échoue ou réussit.

pytest tests/test_route.py::test_home_page_accepts_post_request -vv

ok

------

3.3)	Tester que toute connexion à la page admin est impossible sans user_name = ‘admin’ et password = ‘admin’ ? Vous pouvez par exemple tester la combinaison user_name = ‘wrong’ et password = ‘wrong’. Ce type de test est valide pour le signup et login, … 
Indice : tester.post('/', data={"text":"sayf"}, follow_redirects=True)
test_login.py

Lancement du programme test “test_admin_login_denied_with_wrong_credentials” dans le fichier "test_login.py"

pytest tests/test_login.py::test_admin_login_denied_with_wrong_credentials -vv

ok
---------

3.4)	Tester la combinaison de plusieurs paramètres (avec un seul test) ?
Indice : @pytest.mark.parametrize, doc offic, vid1, vid2
test_parameters.py

Lancement du programme test “test_login_param” dans le fichier "test_parameters.py"

pytest tests/test_parameters.py::test_login_param -vv

ok

--------

3.5)	Retester que toute connexion à la page admin est impossible en utilisant maintenant la notion @pytest.mark.parametrize pour la combinaison user_name=(‘admin’/‘wrong’) et password = (‘admin’/‘wrong’) ?
test_login.py, se limiter au : test_login_param

Lancement du programme test "test_login_param" dans le fichier "test_login.py"

pytest tests/test_login.py::test_login_param -vv

ok

--------

3.6)	Tester que je ne peux pas accéder à la page bienvenue en cliquant sur ok (et ce sans avoir saisi dans le text box) ? Ou encore, l’admin_page (sans avoir passé par la page login)

Lancement du test «test_access_control.py »

python -m pytest -vv tests/test_access_control.py

ok
--------
3.7)	Optimiser les derniers tests en utilisant la notion de fixture (appelé encore test context) ?

J'ai commencé à mettre une fixture dès les premiers tests pour créer un client de test Flask.
Ce client simule un navigateur web pour interagir avec l’application sans la lancer réellement dans un serveur externe (Voir dans les programmes des différents tests).

------

3.8)	Comment exécuter des tests en parallèle ? 
Indice : pip install pytest-xdist ; pytest -n 4 ; Exemple : test_speed.py

Etape d'installation :
1) python -V
2) python -m pytest --version
3) python -m pip install -U pytest-xdist
4) python -m pytest -n 4 -vv (si les programmes de chaque test sont courts)
5) python -m pytest -n auto -vv (si les programmes sont volumineux)
6) python -m pytest --trace-config | findstr xdist

Lancement du programme "test_speed.py"
 ok
...............
3.9)	Couverture du test ? 
Indice : pip install pytest-xdist ; pytest -n 4 ; Exemple : test_speed.py

1) pip install pytest-cov 
2) pytest --cov=server --cov-report=term-missing

Résultat:

----------------------------------------------------------------
Name        Stmts   Miss  Cover   Missing
----------------------------------------------------------------
server.py      59     16    73%   36, 43, 64, 68-74, 79-84, 95
----------------------------------------------------------------
TOTAL          59     16    73%
----------------------------------------------------------------

si on veut combiner vitesse + couverture

pip install pytest-xdist pytest-cov
pytest -n 4 --cov=server --cov-report=term-missing


Résultats observés pour la question 3.8 et 3.9 :

Lancement des programmes des points 3.8 et 3.9
python -m pytest tests/test_speed.py::test_server_starts_fast -vv


Ajout dans pytest.ini

[pytest]
addopts = -q -n 4 --cov=server --cov-report=term-missing
testpaths = tests

Résultat:


Name        Stmts   Miss  Cover   Missing
-----------------------------------------
server.py      59     32    46%   24, 28-38, 43, 47-64, 68-74, 79-84, 95
-----------------------------------------
TOTAL          59     32    46%
............

3.10)	Relancer le dernier test sur Chrome, FireFox et Edge pour être sûr que le site soit compatible avec ces principaux browsers (éventuellement safari) ? 
1è approche : test_selenium_fix_class, 2è approche plus élégante : test_selenium_fixt_params.py
Indice : https://www.blazemeter.com/blog/improve-your-selenium-webdriver-tests-with-pytest

Etape d'installation:
1) pip install selenium
2) python server.py
3) pytest tests/test_selenium_fixt_params.py -v
Pour permettre à selenium de joindre l'app Flask

Faire tourner Flask dans le même process que pytest (un thread), ainsi la couverture compte aussi le code serveur.

Dans "conftest.py" ajouter une fonction "wait_port" et "@pytest.fixture(scope="session", autouse=True)"

.........
3.11)	Approfondissement : Comment afficher le rapport automatiquement juste après la fin du test ? 
Indice : https://stackoverflow.com/questions/52032885/pytest-how-to-display-generated-report-after-test-run/52034116#52034116

Etape d'installation:

1) pip install pytest-html

2) pytest --cov=server --cov-report=html
Pour régler le problème qui a cassé la compatibilité Jinja2 ↔ Flask en installant pytest-html, qui a mis Jinja2 3.1.x.
Or ta version de Flask (probablement 1.x) fait from jinja2 import escape, supprimé depuis Jinja2 3.1 → d’où : ImportError: cannot import name 'escape' from 'jinja2'


3) pip install -U "Flask>=2.2,<3" "Werkzeug>=2.2,<3" "itsdangerous>=2.1,<3" "click>=8.1,<9"
4) Relance les tests: pytest --html=report.html --self-contained-html

5) Pour lancer le rapport html
pytest --html=report.html --self-contained-html --cov=server --cov-report=html -n 4
