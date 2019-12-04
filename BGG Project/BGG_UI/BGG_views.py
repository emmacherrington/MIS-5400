"""
Routes and views for the flask application.
"""
import requests as r
from datetime import datetime
from flask import render_template, Flask
from BGG_UI import app
from bson.json_util import dumps, loads


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Feel free to contact us! (as none of the emails are real)'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='BGG Fall Project',
        year=datetime.now().year,
        message='BY: Shawn Robbins, Emma Cherrington, and Tori Snow'
    )


@app.route('/data')
def data():
    """Renders the data page."""
    raw_data = get_all_games()
    return render_template(
        'data.html',
        title='All The Games',
        message='Here you can see a list of all the games. Click one to see details',
        user_games=loads(raw_data.content)
    )


@app.route('/detail/<string:gameid>')
def detail(gameid):
    """Renders the detail page."""
    raw_data = get_one_game(gameid)
    return render_template(
        'detail.html',
        title='Game Detail',
        game=loads(raw_data.content),
        message='All the deets on the game you selected.'

    )

def get_all_games():
    return r.get("http://localhost:5000/api/v1/games")

def get_one_game(game):
    url = "http://localhost:5000/api/v1/games/" + str(game)
    return r.get(url)

#http://127.0.0.1:5000/api/v1/games