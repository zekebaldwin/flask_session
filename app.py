from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
toolbar = DebugToolbarExtension(app)



RESPONSES_KEY = "responses"

@app.route("/")
def home_page():
    return render_template("base.html", survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def answer():
    answer = request.form.get("answer", None)
    
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:qid>")
def questions(qid):
    responses = session.get(RESPONSES_KEY)
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    if (responses is None):
        return redirect("/")
    if (len(responses) != qid):
        return redirect(f"/questions/{len(responses)}")
    question = survey.questions[qid]
    return render_template("questions.html", qid=qid, question=question)

@app.route("/complete")
def complete():
    return render_template("complete.html")



