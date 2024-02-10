from uuid_extensions import uuid7, uuid7str
from flask import render_template, request, redirect, url_for, Blueprint, current_app
import datetime

pages = Blueprint("habits", __name__, template_folder="templates", static_folder="static")


@pages.context_processor
def add_calc_date_range():
    def days_range(start: datetime.datetime):
        days = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return days
    return {"date_range": days_range}

@pages.route("/")
def home():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    else:
        selected_date = datetime.datetime.today()

    habits_on_date = current_app.db.habits.find({"added": {"$lte": selected_date}})

    completions = [
        habit["habit"] for habit in current_app.db.completions.find({"date": selected_date})
    ]    

    return render_template(
        "home.html", 
        habits=habits_on_date, 
        title="Habit Tracker - Home",
        collections=completions,
        selected_date=selected_date
    )

@pages.route("/add", methods=["GET", "POST"])
def add_habit():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)
    else:
        selected_date = datetime.datetime.today()
        
    if request.method=="POST":
        current_app.db.habits.insert_one({
            "_id": uuid7(as_type='hex'), "added": selected_date, "name": request.form.get("habit")
        })
    return render_template("add_habit.html", title="Habit tracker - Add Habit", selected_date=selected_date)

@pages.route("/completed", methods=['POST'])
def completed():
    date_str = request.form.get('date')
    habit = request.form.get("habitName")
    date = datetime.datetime.fromisoformat(date_str)
    current_app.db.completions.insert_one({"date": date, "habit": habit})
    return redirect(url_for("habits.home", date=date_str))