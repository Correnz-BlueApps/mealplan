from flask import redirect, render_template, session
from functools import wraps
import requests


def error(msg):
    return render_template("error.html", errormsg=msg)


def login_required(f):              # this function is from the cs50 finance project -> https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def recipeById(recipe_id):
    url = f"https://api.chefkoch.de/v2/recipes/{recipe_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        print(f"Request Error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing Error: {e}")
    return None