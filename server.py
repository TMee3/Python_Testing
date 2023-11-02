import json
from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


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
            return render_template(template_name_or_list='welcome.html',
                                   club=found_club[0],
                                   competitions=competitions), 400
        return render_template(template_name_or_list='booking.html',
                               club=found_club[0],
                               competition=found_competition[0],
                               total_places=int(found_competition[0]["numberOfPlaces"]))
    if len(found_club) > 0 and len(found_competition) < 1:
        flash("Something went wrong-please try again")
        return render_template(template_name_or_list='welcome.html',
                               club=found_club[0],
                               competitions=competitions), 400
    return render_template(template_name_or_list='index.html',
                           error="Sorry, you are not authorized to make this request."), 401


@app.route(rule='/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']]
    club = [c for c in clubs if c['name'] == request.form['club']]
    if len(club) > 0 and len(competition) > 0:
        total_places = int(competition[0]["numberOfPlaces"])
        if request.form["places"].isdigit():
            places_required = int(request.form['places'])
        else:
            return render_template(template_name_or_list='booking.html',
                                   club=club[0],
                                   competition=competition[0],
                                   total_places=total_places,
                                   error="Please enter a number between 1 and 12"), 400
        if places_required < 1 or places_required > 12:
            return render_template(template_name_or_list='booking.html',
                                   club=club[0],
                                   competition=competition[0],
                                   total_places=total_places,
                                   error="Please take between 1 and 12 places maximum."), 400
        if places_required > total_places:
            return render_template(template_name_or_list='booking.html',
                                   club=club[0],
                                   competition=competition[0],
                                   total_places=total_places,
                                   error=f"Sorry, there are not enough places left ({total_places})."), 400
        if places_required > int(club[0]['points']):
            return render_template(template_name_or_list='booking.html',
                                   club=club[0],
                                   competition=competition[0],
                                   total_places=total_places,
                                   error=f"You don't have enough points (balance={club[0]['points']} points)."), 400
        competition[0]['numberOfPlaces'] = total_places - places_required
        club[0]['points'] = int(club[0]['points']) - places_required
        flash('Great-booking complete!')
        return render_template(template_name_or_list='welcome.html', club=club[0], competitions=competitions)
    elif len(club) > 0 and len(competition) < 1:
        flash("Something went wrong-please try again")
        return render_template(template_name_or_list='welcome.html', club=club[0], competitions=competitions), 400
    else:
        return render_template(template_name_or_list='index.html',
                               error="Sorry, you are not authorized to make this request."), 401


@app.route(rule='/clubs', methods=['GET'])
def get_list_of_clubs():
    return render_template(template_name_or_list='clubs.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
