import sqlite3
import os

from flask import Flask, g
import json
import requests

app = Flask(__name__)

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

# Create the recipes table
with app.app_context():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            previewImageUrlTemplate TEXT
        );
    ''')
    db.commit()

# Categories of recipes, that are healty and fast 
QUERY_ALTERATIONS = [
    "12",
    "13",
    "21",
    "22",
    "56",
    "58",
    "64",
    "65",
    "66",
]

# Function to call the chefkoch api
def callAPI(offset, tags):
    url = f"https://api.chefkoch.de/v2/recipes?limit=50&offset={offset}&tags={tags}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        print(f"Request Error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing Error: {e}")
    return None

# Loop the maximum amount of recipes, that the API will provide
with app.app_context():
    for alteration in QUERY_ALTERATIONS:
        print(f"geting recipes from the category {QUERY_ALTERATIONS}")
        for i in range(20):
            data = callAPI(i * 50, alteration)
            for a in data.get("results"):
                recipe = a.get("recipe")
                if recipe.get("isPlus") == False and recipe.get("isPremium") == False:
                    db = get_db()
                    db.execute("INSERT OR IGNORE INTO recipes (id, title, previewImageUrlTemplate) VALUES (?, ?, ?);", (
                        int(recipe.get("id")),
                        recipe.get("title"),
                        json.dumps(recipe.get("previewImageUrlTemplate")).replace("<format>", "crop-640x360"),
                    ))
                    db.commit()

# Create the other tables for the website
with app.app_context():
    db = get_db()
    db.execute('''
        CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL);
        CREATE TABLE favorites ( id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, recipeId INTEGER NOT NULL REFERENCES recipes(id), userId INTEGER NOT NULL REFERENCES users(id) );
        CREATE TABLE weeks ( id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, json TEXT NOT NULL, userId INTEGER NOT NULL REFERENCES users(id) );
    ''')
    db.commit()
    print("database setup done.")