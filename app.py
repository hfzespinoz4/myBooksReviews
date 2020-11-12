import os
from flask import (Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import flask_pymongo
from bson.objectId import objectId
from werkseug.security import generate_password_hash, check_password_hash
if os.path.exist("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/reviews")
def get_reviews():
    return render_template("reviews.html")

