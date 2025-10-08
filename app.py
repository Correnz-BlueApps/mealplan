from flask import Flask, g, render_template, request
from flask_session import Session
import os
import random
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import error, recipeById

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
        table = db.execute("SELECT id FROM recipesRawV2;").fetchall()
        data = recipeById(random.choice(table)[0])
        return render_template("index.html", data = data)

# Manage Account and view favorite recipes
@app.route("/account")
def account():
    return error()

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return error()
    
    else:
        return error()

# Logout
@app.route("/logout")
def logout():
    return 404

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if not username or not password1 or not password2:
            return error("Fehler.")
        
        if password1 != password2:
            return error("Gib bitte zwei Mal das selbe Passwort ein.")
        
        with app.app_context():
            db = get_db()
            
            if len(db.execute("SELECT username FROM users WHERE username = ?;", [username]).fetchall()) > 0:
                return error("Dieser Benutzername ist schon vergeben.")
            
            db.execute("INSERT INTO users (username, password) VALUES (?, ?);", [username, generate_password_hash(password1)])
            db.commit()
            return render_template("index.html")        ### TODO: bessere Startseite
        
    else:
        return render_template("register.html")

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
