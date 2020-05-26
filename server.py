from flask import Flask, render_template, request, redirect, url_for
import data_handler
import connection

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_questions():
    all_question = data_handler.get_all_question()
    sorted_questions_by_date = sorted(all_question, key=lambda i: i['submission_time'])
    return render_template("list.html", all_question=sorted_questions_by_date, header=data_handler.DATA_HEADER)

@app.route('/add_question', methots=['post'])
def add_question():
    my_list = []
    if request.method == 'POST':
        question = request.form
        for value in question.values():
            my_list.append(value)
        connection.write_csv_file(question.csv, my_list)
    return render_template("add_question", header=data_handler.DATA_HEADER)


if __name__ == "__main__":
    app.run(debug=True)
