import json
from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for


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


@app.route(rule='/showSummary', methods=['POST'])
def show_summary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    if len(club) > 0:
        return render_template(template_name_or_list='welcome.html', club=club[0], competitions=competitions)
    else:
        return render_template(template_name_or_list='index.html', error="Sorry, that email wasn't found."), 401


@app.route(rule='/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club]
    found_competition = [c for c in competitions if c['name'] == competition]
    if len(found_club) > 0 and len(found_competition) > 0:
        today_date = datetime.now()
        competition_date = datetime.strptime(found_competition[0]["date"], "%Y-%m-%d %H:%M:%S")
        if competition_date < today_date:
            flash("This competition is already over.")
            return (render_template(template_name_or_list='welcome.html', club=found_club[0], competitions=competitions)
                    , 400)
        return render_template(template_name_or_list='booking.html',
                               club=found_club[0],
                               competition=found_competition[0],
                               total_places=int(found_competition[0]["numberOfPlaces"]))
    elif len(found_club) > 0 and len(found_competition) < 1:
        flash("Something went wrong-please try again")
        return render_template(template_name_or_list='welcome.html', club=found_club[0], competitions=competitions), 400
    else:
        return render_template(template_name_or_list='index.html',
                               error="Sorry, you are not authorized to make this request."), 401


@app.route(rule='/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    total_places = int(competition["numberOfPlaces"])
    if request.form["places"].isdigit():
        places_required = int(request.form['places'])
    else:
        return render_template(template_name_or_list='booking.html',
                               club=club,
                               competition=competition,
                               total_places=total_places,
                               error="Please enter a number between 1 and 12"), 400
    if places_required < 1 or places_required > 12:
        return render_template(template_name_or_list='booking.html',
                               club=club,
                               competition=competition,
                               total_places=total_places,
                               error="Please take between 1 and 12 places maximum."), 400
    if places_required > total_places:
        return render_template(template_name_or_list='booking.html',
                               club=club,
                               competition=competition,
                               total_places=total_places,
                               error=f"Sorry, there are not enough places left ({total_places})."), 400
    if places_required > int(club['points']):
        return render_template(template_name_or_list='booking.html',
                               club=club,
                               competition=competition,
                               total_places=total_places,
                               error=f"You don't have enough points (balance={club['points']} points)."), 400
    competition['numberOfPlaces'] = total_places - places_required
    flash('Great-booking complete!')
    return render_template(template_name_or_list='welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))