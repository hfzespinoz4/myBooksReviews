import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
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
    reviews = mongo.db.reviews.find()
    return render_template("reviews.html", reviews=reviews)


@app.route("/myreviews")
def get_myreviews():
    # reviews = mongo.db.reviews.find()
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


@app.route("/register", methods=["GET", "POST"])
def get_register():
    if request.method == "POST":
        # checking if the usename already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("register-username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("get_register"))

        register = {
            "email": request.form.get("register-email"),
            "username": request.form.get("register-username").lower(),
            "password": generate_password_hash(request.form.get("register-password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("register-username").lower()
        flash("Registration Succesful")
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
