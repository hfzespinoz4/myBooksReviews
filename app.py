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
# load reviews in database
@app.route("/reviews")
def get_reviews():
    reviews = list(mongo.db.reviews.find())
    return render_template("reviews.html", reviews=reviews)


# Show reviews created by current user
@app.route("/myreviews")
def get_myreviews():
    usr = session["user"]
    # search for current user review in database
    myreviews = list(mongo.db.reviews.find({"user": usr}))
    if usr == "":
        return render_template("login.html")
    else:
        return render_template("myreviews.html", myreviews=myreviews)


# edit review function
@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    # validate method
    if request.method == "POST":
        # get system date
        today = date.today()
        submit = {
            "title": request.form.get("editreview-title"),
            "author": request.form.get("editreview-author"),
            "cover": request.form.get("editreview-cover"),
            "last_mod": today.strftime("%d/%m/%Y"),
            "review": request.form.get("editreview-review")
        }
        # edit review in database
        mongo.db.reviews.update({"_id": ObjectId(review_id)}, submit)
        # display confirmation message
        flash("Review Successfully Updated")

    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    return render_template("editreview.html", review=review)


# Create review function
@app.route("/create-review", methods=["GET", "POST"])
def create_review():
    # get username from session cookie
    usr = session["user"]
    myreviews = list(mongo.db.reviews.find({"user": usr}))
    # get system date
    today = date.today()

    newreview = {
        "title": request.form.get("new-title"),
        "author": request.form.get("new-author"),
        "cover": request.form.get("new-cover"),
        "user": session["user"],
        "creation_date": today.strftime("%d/%m/%Y"),
        "last_mod": today.strftime("%d/%m/%Y"),
        "review": request.form.get("new-review"),
        "active": "true"
    }
    # insert review in database
    mongo.db.reviews.insert_one(newreview)
    return render_template("myreviews.html", myreviews=myreviews)


# User registration function
@app.route("/register", methods=["GET", "POST"])
def get_register():
    if request.method == "POST":
        # checking if the usename already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("register-username").lower()})

        # If user is registered reload page
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("get_register"))

        # If user isn´t registered create new user
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
        return redirect(url_for("get_reviews"))
    return render_template("register.html")


# Login function
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


# display profile function
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("get_login"))


# Logout function
@app.route("/logout")
def get_logout():
    # Removing user from session cookie
    flash("You have logged out")
    session.pop("user")
    return redirect(url_for("get_login"))


# Delete Review function
@app.route("/delete_review/<review_id>")
def delete_review(review_id):
    # delete review with an specific id
    mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    # show confirmation message
    flash("Review Successfully Deleted!")
    # render reviews page
    return redirect(url_for("get_reviews"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
