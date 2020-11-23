import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
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
    reviews = list(mongo.db.reviews.find())
    return render_template("reviews.html", reviews=reviews)


@app.route("/myreviews")
def get_myreviews():
    usr = session["user"]
    myreviews = list(mongo.db.reviews.find({"user": usr}))
    return render_template("myreviews.html", myreviews=myreviews)


@app.route("/profile")
def get_profile():
    usr = session["user"]
    profile = mongo.db.users.find({"user": usr})
    return render_template("profile.html", profile=profile)


@pp.route("/create-review", methods=["GET", "POST"])
def create_review():
    newreview = {
        "title": request.form.get("register-email"),
        "author": request.form.get("register-username").lower(),
        "cover": generate_password_hash(
        "user":"hzunigaes"
        "creation_date: "10/10/2020"
        "last_mod:"10/10/2020"
        "review:"Este libro es tremendo!"
        "active:"true
        }
        mongo.db.reviews.insert_one(newreview)

    }


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
            "password": generate_password_hash(
                request.form.get("register-password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("register-username").lower()
        flash("Registration Succesful")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def get_login():
    if request.method == "POST":
        # Verifiy if username is registered in mongodb
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("login-username")})

        if existing_user:
            # Verify hashed password matches with db record
            if check_password_hash(
                existing_user["password"], request.form.get("login-password")):
                session["user"] = request.form.get("login-username").lower()
                flash("Welcome, {}" .format(
                    request.form.get("login-username")))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                # Invalid Password
                flash("Incorrect Username and/or Password, please verify")
                return redirect(url_for("get_login"))
        else:
            # usernae doesn´t exist
            flash("Incorrect Username and/or Password, please verify")
            return redirect(url_for("get_login"))
    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("get_login"))


@app.route("/logout")
def get_logout():
    # Removing user from session cookie
    flash("You have logged out")
    session.pop("user")
    return redirect(url_for("get_login"))




if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
