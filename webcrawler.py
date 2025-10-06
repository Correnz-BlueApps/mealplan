import sqlite3
import os

from flask import Flask, g, render_template
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


with app.app_context():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS recipesRaw (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TEXT,
            difficulty INTEGER,
            is_plus BOOLEAN,
            is_premium BOOLEAN,
            nutrition TEXT,
            preparationTime INTEGER,
            previewImageUrlTemplate TEXT,
            rating REAL,
            ratingCount INTEGER,
            siteUrl TEXT
        );
    ''')
    db.commit()

QUERY_ALTERATIONS = [
    "",
]


def callAPI(offset, alteration):
    url = f"https://api.chefkoch.de/v2/recipes?tags=21&limit=50&offset={offset}{alteration}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        print(f"Request Error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing Error: {e}")
    return None

with app.app_context():
    for alteration in QUERY_ALTERATIONS:
        for i in range(20):
            data = callAPI(i * 50, alteration)
            for a in data.get("results"):
                recipe = a.get("recipe")
                db = get_db()
                db.execute('''
                    INSERT OR IGNORE INTO recipesRaw (
                        id, title, created_at, difficulty, is_plus, is_premium,
                        nutrition, preparationTime, previewImageUrlTemplate,
                        rating, ratingCount, siteUrl
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                ''', (
                    int(recipe.get("id")),
                    recipe.get("title"),
                    recipe.get("createdAt"),
                    recipe.get("difficulty"),
                    recipe.get("isPlus"),
                    recipe.get("isPremium"),
                    json.dumps(recipe.get("nutrition")),
                    recipe.get("preparationTime"),
                    json.dumps(recipe.get("previewImageUrlTemplate")).replace("<format>", "crop-640x360"),
                    recipe.get("rating").get("rating"),
                    recipe.get("rating").get("numVotes"),
                    recipe.get("siteUrl")
                ))
                db.commit()