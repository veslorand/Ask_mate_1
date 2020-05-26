from flask import Flask, render_template, request, redirect, url_for
import data_handler

app = Flask(__name__)


@app.route("/")
@app.route("/list")
@app.route("/question")
def list_questions():
    all_question = data_handler.get_all_question()
    return render_template("list.html", all_question=all_question)


def find_question():
    question = data_handler.find_question_by_id(1)
    answer = data_handler.find_answer_by_id(1)
    return render_template("question.html", question=question, answer=answer)


if __name__ == "__main__":
    app.run(debug=True)
