from flask import Flask, g, render_template
from flask_session import Session
import random
import sqlite3
import os


from helpers import recipeById

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



### Database Setup ###

DATABASE = 'database.db'

def get_db():        ## From: https://flask.palletsprojects.com/en/stable/patterns/sqlite3/
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext        ## From: https://flask.palletsprojects.com/en/stable/patterns/sqlite3/
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



### Routes ###

@app.route("/")
def index():
    with app.app_context():
        db = get_db()
        table = db.execute("SELECT id FROM recipesRaw;").fetchall()
        data = recipeById(random.choice(table)[0])
        return render_template("index.html", data = data)
    
# Manage Account and view favorite recipes
@app.router("/account")
def account():
    return 404

# Login
@app.route("/login", methodes=["GET", "POST"])
def login():
    return 404

# Logout
@app.router("/logout")
def logout():
    return 404

# Register
@app.router("/register", methodes=["GET", "POST"])
def register():
    return 404

# Get 7 dishes to cook for the week
@app.route("/wochenplan")
def wochenplan():
    with app.app_context():
        db = get_db()
        table = db.execute("SELECT id FROM recipesRaw;").fetchall()
        data = []

        for i in range(7):
            recipe = recipeById(random.choice(table)[0])
            #recipe["rating"]["numVotes2"] = "(" + recipe["rating"]["numVotes"] + ")"
            recipe["image"] = recipe.get("previewImageUrlTemplate").replace("<format>", "crop-640x360")
            data.append(recipe)

        return render_template("wochenplan.html", data = data)
