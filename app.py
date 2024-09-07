from flask import Flask, request, render_template,  redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "12345"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []

@app.route("/")
def show_root():
    """Shows the root page"""
    title = surveys["satisfaction"].title
    instructions = surveys["satisfaction"].instructions
    return render_template("root.html", title=title, instructions=instructions, question_id=0)

@app.route("/questions/<int:question_id>")
def show_question(question_id):
    """Shows the question page"""
    if len(responses) == len(surveys["satisfaction"].questions):
        """If the user tries to answer a question after the last question, redirect to the thanks page"""
        flash("You have already answered all the questions", "error")
        return redirect("/thanks")

    if question_id > len(surveys["satisfaction"].questions):
        """If the user tries to access a question that doesn't exist, 
        redirect to the thanks page or the question they should be on"""
        if len(responses) == len(surveys["satisfaction"].questions):
            flash("You have already answered all the questions", "error")
            return redirect("/thanks")
        else:
            flash("That question doesn't exist", "error")
            return redirect(f"/questions/{len(responses)}")
        
    if len(responses) != question_id:
            """If the user tries to skip a question, redirect to the current question"""
            flash("Please answer the current question", "error")
            return redirect(f"/questions/{len(responses)}")
    
    question = surveys["satisfaction"].questions[question_id].question
    choices = surveys["satisfaction"].questions[question_id].choices
    return render_template("questions.html", question=question, question_id=question_id, choices=choices)


@app.route("/answer", methods=["POST"])
def answer_question():
    """Answers the question"""
    answer = request.form.get("answer")
    responses.append(answer)
    if len(responses) == len(surveys["satisfaction"].questions):
        return redirect("/thanks")
    return redirect(f"/questions/{len(responses)}")

@app.route("/thanks")
def show_thanks():
    """Shows the thanks page"""
    if len(responses) != len(surveys["satisfaction"].questions):
        flash("Please answer all the questions", "error")
        return redirect(f"/questions/{len(responses)}")
    return render_template("thanks.html")

