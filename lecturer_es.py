from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import json

with open('db.json') as f:
    data = json.load(f)

app = Flask(__name__)

student_info = {
    "Name": "",
    "Matric_Number": "",
    "Year": "",
    "Course": "",
}

curr_question = list(data.keys())[0]
curr_response = data[curr_question]
final_answer = ""


@ app.route('/')
def home():
    curr_time = datetime.now()
    hour = int(curr_time.strftime("%H"))

    if hour >= 0 and hour < 12:
        message = "Morning"
    elif hour >= 12 and hour < 17:
        message = "Afternoon"
    else:
        message = "Evening"

    return render_template("home.html", message=message)


@ app.route("/get-to-know", methods=["GET", "POST"])
def get_info():
    if request.method == "POST":
        student_info["Name"] = request.form["name"]
        student_info["Matric_Number"] = request.form["matric-number"]
        student_info["Year"] = request.form.get("year-of-study")
        student_info["Course"] = request.form.get("course")
        return redirect("/introduction")

    return render_template("information.html")


@ app.route("/introduction", methods=["GET", "POST"])
def intro():
    if request.method == "POST":
        response = request.form["response-button"]

        global curr_response
        global curr_question

        next_decision = curr_response[response]
        question = list(next_decision.keys())[0]
        next_responses = next_decision[question]
        curr_response = next_responses
        curr_question = question

        return redirect("/question")

    else:
        responses = list(curr_response.keys())
        return render_template("introduction.html", name=student_info["Name"], main_question=curr_question, responses=responses)


@ app.route("/question", methods=["GET", "POST"])
def questions():
    if request.method == "POST":
        response = request.form["response-button"]

        global curr_response
        global curr_question
        global final_answer

        next_decision = curr_response[response]

        if isinstance(next_decision, dict):
            question = list(next_decision.keys())[0]
            curr_question = question
            next_responses = next_decision[question]
            curr_response = next_responses

            return render_template("questions.html", main_question=question, responses=next_responses)
        else:
            curr_question = response
            final_answer = next_decision
            return redirect("/answer")

    return render_template("questions.html", main_question=curr_question, responses=curr_response)


@ app.route("/answer", methods=["GET", "POST"])
def answer():
    if request.method == "POST":

        global curr_question
        global curr_response

        curr_question = list(data.keys())[0]
        curr_response = data[curr_question]

        return redirect("/introduction")

    return render_template("answer.html", question=curr_question, answer=final_answer)


app.run(debug=True)
