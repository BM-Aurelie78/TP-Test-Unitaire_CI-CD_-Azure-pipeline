import json
from flask import Flask, render_template, request, redirect, url_for, session, flash


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form.get('email', '').strip()

    # 🔒 Si aucun email n’est saisi → redirection ou erreur
    if not email:
        return redirect(url_for('index')), 302  # ou ( "return '', 400" si tu veux une erreur HTTP pure )

    club = next((c for c in clubs if c['email'] == email), None)
    if club is None:
        return redirect(url_for('index')), 302  # ou 400 si tu veux une erreur claire

    return render_template('welcome_1.html', club=club, competitions=competitions), 200
    
@app.route('/ConnexionAdmin', methods=['GET'])
def ConnexionAdmin():
    # Affiche la page de connexion admin
    return render_template('ConnexionAdmin.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')

        # Vérifie les identifiants
        if email == 'admin@admin.com' and password == 'admin':
            session['is_admin'] = True
            return render_template('admin.html'), 200
        else:
            # Échec d'authentification → accès refusé
            return render_template('ConnexionAdmin.html'), 403

    # 🔒 Accès direct sans être connecté → 403 (pas autorisé)
    if not session.get('is_admin'):
        return "Accès refusé : vous devez être connecté.", 403

    # ✅ Accès autorisé
    return render_template('admin.html'), 200

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome_1.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome_1.html', club=club, competitions=competitions)


# TODO: Add route for points display


# @app.route('/logout')
# def logout():
#     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)    