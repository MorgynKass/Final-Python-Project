from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Protein, Goal
from . import db
from datetime import datetime

tracker = Blueprint("tracker", __name__)


@tracker.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template("tracker.html", user=current_user)


@tracker.route("/update_protein", methods=["POST"])
@login_required
def update_protein():
    user_input = request.form.get("protein")

    id = current_user.id

    protein = Protein.query.filter_by(id=id).first()

    if user_input == "":
        user_input = protein.daily_protein

    new_data = protein.daily_protein + float(user_input)
    protein.daily_protein = new_data
    db.session.commit()

    change_info()

    return render_template("tracker.html", user=current_user)


@tracker.route("/update_goal", methods=["POST"])
@login_required
def update_goal():
    goal = request.form.get("goal")

    id = current_user.id

    db_goal = Goal.query.filter_by(id=id).first()
    if goal == "":
        goal = db_goal.goal

    db_goal.goal = goal
    db.session.commit()

    change_info()

    return render_template("tracker.html", user=current_user)


@tracker.route("/reset", methods=["POST"])
@login_required
def reset():
    id = current_user.id

    db_goal = Goal.query.filter_by(id=id).first()
    protein = Protein.query.filter_by(id=id).first()

    db_goal.percent = 0
    db_goal.remaining_value = db_goal.goal
    protein.daily_protein = 0
    db.session.commit()

    return render_template("tracker.html", user=current_user)


def change_info():
    """Updates user's percent and remainder feedback on the page using the goal and protein data."""

    id = current_user.id

    db_goal = Goal.query.filter_by(id=id).first()
    protein = Protein.query.filter_by(id=id).first()

    if protein.daily_protein == 0 or db_goal.goal == 0:
        new_percent = protein.daily_protein
    else:
        new_percent = round((protein.daily_protein / db_goal.goal * 100), 2)
    new_remainder = db_goal.goal - protein.daily_protein
    db_goal.remaining_value = new_remainder
    db_goal.percent = new_percent
    db.session.commit()

    return
