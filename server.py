from flask import Flask, redirect, request, render_template, session, flash, jsonify, request_finished
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

from model import connect_to_db, db, User, Goal

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

app.secret_key = "ABC"

@app.route("/")
def show_homepage():
    """Displays homepage"""

    return render_template("home.html")

@app.route("/login", methods=["POST"])
def log_in():
    """Logs in an existing user"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("We couldn't find you in our records!")
        return redirect("/")

    if user.password != password:
        flash("Your password is incorrect. Please try again")
        return redirect("/")

    session["user_id"] = user.user_id

    return redirect(f"/goals/{user.user_id}")


@app.route("/register", methods=["POST"])
def add_user():
    """Handles intake questions for new user"""

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    user = User(name=name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.user_id

    return redirect(f"/goals/{user.user_id}")


@app.route("/goals/<int:user_id>")
def show_goals(user_id):
    """Displays user's goal page"""

    user_id = session.get("user_id")
    user = User.query.filter_by(user_id=user_id).first()
    goals = Goal.query.filter_by(user_id=user_id).all()

    return render_template("goals.html",
                                user=user,
                                goals=goals)


@app.route("/add-goal", methods=["POST"])
def add_goal():
    """Adds a goal to the db and displays in goal section"""
    user_id = session.get("user_id")
    goal = request.form.get("goal")

    new_goal = Goal(user_id=user_id, goal=goal)

    db.session.add(new_goal)
    db.session.commit()

    flash("Goal added!")

    return redirect(f"/goals/{user_id}")


@app.route("/edit-goal", methods=["POST"])
def edit_goal():
    """Edits an existing goal in the db"""
    user_id = session.get("user_id")
    goal_id = request.form.get("id")
    date = request.form.get("date")
    text = request.form.get("goal")

    user_goal = (Goal.query.filter_by(user_id=user_id, 
                                    goal_id=goal_id).first())

    user_goal.entry_date = date
    user_goal.goal = text 
    db.session.commit()

    return redirect(f"/goals/{user_id}")


@app.route("/logout")
def logout():
    """Logs out current user"""

    del session["user_id"]
    flash("Logged out")

    return redirect("/")


if __name__ == "__main__":
    app.debug = False

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    connect_to_db(app)

    app.run(host="0.0.0.0")
