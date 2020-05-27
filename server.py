from flask import Flask, render_template, request, redirect

import connection
import data_handler

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_questions():
    all_question = data_handler.get_all_question()
    sorted_questions_by_date = sorted(all_question, key=lambda i: i['submission_time'])
    k = [i for i in request.values.values()]
    for i in k:
        print(i)
    return render_template("question_list.html", all_question=sorted_questions_by_date, header=data_handler.QUESTIONS_HEADER)


@app.route("/question/<question_id>")
def question(question_id):
    line = data_handler.get_questions_by_id(question_id, data_handler.QUESTION_FILE)
    all_answer = data_handler.get_all_answer()
    sorted_answer_by_vote = sorted(all_answer, key=lambda i: i['vote_number'])
    return render_template("answer_list.html", question=line, header=data_handler.ANSWERS_HEADER, all_answer=sorted_answer_by_vote)


@app.route('/add_new_question', methods=['POST', 'GET'])
def add_new_question():
    # id,submission_time,view_number,vote_number,title,message,image
    if request.method == 'POST':
        new_question_data = data_handler.create_question_form(request.form.values())
        connection.append_csv_file(data_handler.QUESTION_FILE, new_question_data)
        return redirect("/question/" + new_question_data[0])
    return render_template("add_new_question.html", header=data_handler.QUESTIONS_HEADER)


@app.route('/question/<question_id>/new-answer', methods=['POST', 'GET'])
def add_new_answer(question_id):
    # id, submission_time, vote_number, question_id, message, image
    if request.method == 'POST':
        new_answer_data = data_handler.create_answer_form(request.form.values(), question_id)
        connection.append_csv_file(data_handler.ANSWER_FILE, new_answer_data)
        return redirect('/question/' + question_id)
    return render_template("add_new_answer.html", header=data_handler.ANSWERS_HEADER)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    all_question = data_handler.get_all_question()
    connection.write_csv_file(data_handler.QUESTION_FILE, all_question, data_handler.QUESTIONS_HEADER, question_id)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
