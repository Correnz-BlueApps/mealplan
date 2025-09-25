import os
from flask import Flask, render_template
from flask_session import Session
from helpers import recipeById

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():

    data = recipeById("1075481213257527")

    return render_template("index.html", data = data)
