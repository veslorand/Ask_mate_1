from flask import Flask, render_template, request, redirect, url_for
import data_handler

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_questions():
    all_question = data_handler.get_all_question()
    sorted_questions_by_date = sorted(all_question, key=lambda i: i['submission_time'])
    return render_template("list.html", all_question=sorted_questions_by_date, header=data_handler.DATA_HEADER)


if __name__ == "__main__":
    app.run(debug=True)
