from flask import Flask, render_template, request, redirect, url_for
import data_handler

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_questions():
    all_question = data_handler.get_all_question()
    return render_template("list.html", all_question=all_question)


if __name__ == "__main__":
    app.run()
