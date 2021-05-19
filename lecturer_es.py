from flask import Flask, render_template, url_for
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def hello_world():
    curr_time = datetime.now()
    hour = int(curr_time.strftime("%H"))

    if hour >= 0 and hour < 12:
        message = "Morning"
    elif hour >= 12 and hour < 17:
        message = "Afternoon"
    else:
        message = "Evening"

    return render_template("home.html", message=message)


app.run(debug=True)
