from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

app = Flask(__name__)

student_info = {
    "Name": "",
    "Matric_Number": "",
    "Year": "",
    "Course": "",
}


@app.route('/')
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


@app.route("/get-to-know", methods=["POST", "GET"])
def get_info():
    if request.method == "POST":
        student_info["Name"] = request.form["name"]
        student_info["Matric_Number"] = request.form["matric-number"]
        student_info["Year"] = request.form.get("year-of-study")
        student_info["Course"] = request.form.get("course")
        print(student_info)
    return render_template("information.html")


app.run(debug=True)
