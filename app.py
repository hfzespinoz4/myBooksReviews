import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


# Creating the app
app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Creating an instance of PyMongo and parsing the application
mongo = PyMongo(app)


@app.route("/")
@app.route("/reviews")
def get_reviews():
    users = mongo.db.users.find()
    return render_template("reviews.html", users=users)


@app.route("/myreviews")
def get_myreviews():
    return render_template("myreviews.html")


@app.route("/profile")
def get_profile():
    users = mongo.db.users.find()
    return render_template("profile.html", users=users)


@app.route("/login")
def get_login():
    return render_template("login.html")


@app.route("/logout")
def get_logout():
    return render_template("logout.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
