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

        if response == "I want to develop a Database":
            return redirect("/develop-db")

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

    if "question" in request.args:
        return render_template("answer.html", question=request.args["question"], answer=request.args["answer"])
    return render_template("answer.html", question=curr_question, answer=final_answer)


@ app.route("/develop-db", methods=["GET", "POST"])
def develop_db():
    db_data = data['What would you like to learn today?']['I want to develop a Database']
    db_rules = []
    db_rules.extend(rule for rule in db_data['sql'])
    db_rules.extend(rule for rule in db_data['nosql'])

    if request.method == "POST":
        rule_ans = request.form.to_dict()

        ans_text = {'sql': 'Database that you should use is SQL Database. Sample of SQL database are MySQL, Oracle and PostgreSQL.',
                    'nosql': 'Database that you should use is NoSQL Database. Sample of NoSQL database are MongoDB and Firestore.',
                    'Not valid': 'There is no database type that can fulfill your requirements. Please try again.',
                    None: 'Please insert atleast one requirement and try again.'}
        result_db = None
        for rule in db_rules:
            if rule_ans[rule] == 'Yes':
                if rule in db_data['sql']:
                    if result_db is None:
                        result_db = 'sql'
                    elif result_db != 'sql':
                        result_db = 'Not valid'
                        break
                else:
                    if result_db is None:
                        result_db = 'nosql'
                    elif result_db != 'nosql':
                        result_db = 'Not valid'
                        break
            elif rule_ans[rule] == 'No':
                if rule in db_data['sql']:
                    if result_db is None:
                        result_db = 'nosql'
                    elif result_db == 'sql':
                        result_db = 'Not valid'
                        break
                else:
                    if result_db is None:
                        result_db = 'sql'
                    elif result_db == 'nosql':
                        result_db = 'Not valid'
                        break
        result_db = ans_text[result_db]
        return redirect(url_for('.answer', question="What type of Database should I use?", answer=result_db))
    return render_template("develop_db.html", db_rules=db_rules)


app.run(debug=True)
