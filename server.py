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

@app.route('/add_question', methods=['post'])
def add_question():
    my_list = []
    if request.method == 'POST':
        new_question = request.form
        for value in new_question.values():
            my_list.append(value)
        connection.write_csv_file(data_handler.QUESTION_FILE, my_list)
    return render_template("add_question.html", header=data_handler.DATA_HEADER)


@app.route("/question/<question_id>")
def question(question_id):
    line = data_handler.get_questions_by_id(question_id, data_handler.QUESTION_FILE)
    all_answer = data_handler.get_all_answer()
    sorted_answer_by_vote = sorted(all_answer, key=lambda i: i['vote_number'])
    return render_template("question.html", question=line, header=data_handler.QUESTION_HEADER, all_answer=sorted_answer_by_vote)


# @app.route("/question/add_question")
# def add_question():
#     return render_template("add_question.html")


if __name__ == "__main__":
    app.run(debug=True)
