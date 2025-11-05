from flask import Flask, g, redirect, render_template, request, session
from flask_session import Session
import json
import os
import random
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import error, login_required, recipeById

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
    return render_template("index.html")

# Manage Account and view favorite recipes
@app.route("/account")
@login_required
def account():
    with app.app_context():

        weekObjs = get_db().execute("SELECT * FROM weeks WHERE userId = ?;", [session["user"]]).fetchall()
        weeks = []
        for weekObj in weekObjs:
            week = {
                "id": weekObj[0],
                "name": weekObj[1],
                "recipes": []
            }
            for id in json.loads(weekObj[2]):
                recipe = recipeById(id)
                if recipe and recipe["id"]:
                    recipe["image"] = recipe.get("previewImageUrlTemplate").replace("<format>", "crop-640x360")
                week["recipes"].append(recipe)
            weeks.append(week)
            

        idList = get_db().execute("SELECT * FROM favorites WHERE userId = ?;", [session["user"]]).fetchall()
        recipes = []
        for entry in idList:
            recipe = recipeById(entry[1])
            recipe["image"] = recipe.get("previewImageUrlTemplate").replace("<format>", "crop-640x360")
            recipes.append(recipe)
        print(weeks)
        return render_template("account.html", recipes = recipes, weeks = weeks)

# Add recipe to favorites
@app.route("/favoriteRecipeAdd", methods=["POST"])
@login_required
def favoriteRecipeAdd():
    with app.app_context():
        db = get_db()
        if len(db.execute("SELECT * FROM favorites WHERE userId = ? AND recipeId = ?;", [session["user"], request.json.get("recipeId")]).fetchall()) == 0:
            db.execute("INSERT INTO favorites (userId, recipeId) VALUES (?, ?);", [session["user"], request.json.get("recipeId")])
            db.commit()
        return {"answer": "success"}
    
# Remove recipe from Favorites
@app.route("/favoriteRecipesRemove", methods=["POST"])
@login_required
def favoriteRecipeRemove():
    with app.app_context():
        db = get_db()
        db.execute("DELETE FROM favorites WHERE userId = ? AND recipeId = ?;", [session["user"], request.json.get("recipeId")])
        db.commit()
        return {"answer": "success"}


# Get all favorites recipes
@app.route("/getAllFavoriteRecipes")
@login_required
def getAllFavoriteRecipes():
    with app.app_context():
        db = get_db()
        idList = db.execute("SELECT * FROM favorites WHERE userId = ?;", (session["user"]))
        return "0"

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return error("Fehler.")
        
        with app.app_context():
            db = get_db()
            dbEntry = db.execute("SELECT * FROM users WHERE username = ?;", [username]).fetchall()

            if len(dbEntry) != 1 or not check_password_hash( dbEntry[0][2], password):
                return error("Falscher Name oder falsches Passwort.")
            
            session["user"] = dbEntry[0][1]
            return redirect("/wochenplan")

    else:
        return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# One Recipe
@app.route("/oneRecipe")
@login_required
def oneRecipe():
    with app.app_context():
        table = get_db().execute("SELECT id FROM recipesRaw;").fetchall()
        recipe = recipeById(random.choice(table)[0])
        recipe["image"] = recipe.get("previewImageUrlTemplate").replace("<format>", "crop-640x360")
        return recipe


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

            user = db.execute("SELECT * FROM users WHERE username = ?;", [username]).fetchone()
            session["user"] = user[1]
            return redirect("/")        ### TODO: bessere Startseite
        
    else:
        return render_template("register.html")

# Save current week to account
@app.route("/weekAdd", methods=["POST"])
@login_required
def weekAdd():
    with app.app_context():
        data = json.loads(request.data.decode('utf-8'))     #request.data was datatype bytes. solution from: https://stackoverflow.com/questions/6541767/python-urllib-error-attributeerror-bytes-object-has-no-attribute-read
        db = get_db()
        db.execute("INSERT INTO weeks (name, json, userId) VALUES (?, ?, ?);", [data.get("name"), json.dumps(data.get("recipes")), session["user"]])
        db.commit()
        return {"answer": "success"}

@app.route("/weekRemove", methods=["POST"])
@login_required
def weekRemove():
    with app.app_context():
        data = json.loads(request.data.decode('utf-8'))
        db = get_db()
        db.execute("DELETE FROM weeks WHERE id = ?;", [data.get("id")])
        db.commit()
        return {"answer": "success"}

# Get 7 dishes to cook for the week
@app.route("/wochenplan")
@login_required
def wochenplan():
    with app.app_context():
        data = []
        table = get_db().execute("SELECT id FROM recipesRaw;").fetchall()

        for i in range(7):
            recipe = recipeById(random.choice(table)[0])
            recipe["image"] = recipe.get("previewImageUrlTemplate").replace("<format>", "crop-640x360")
            data.append(recipe)

        return render_template("wochenplan.html", data = data)
