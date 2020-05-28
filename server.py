import os

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

import connection
import data_handler

app = Flask(__name__)
UPLOAD_FOLDER = '/home/veslorandpc/Desktop/projects/Ask_mate_1'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import speech_recognition as sr


@app.route("/")
@app.route("/list")
def list_questions():
    all_question = data_handler.get_all_question()
    if request.args:
        if request.args.get('order_direction') == "desc":
            sorted_questions_by_date = sorted(all_question, key=lambda i: i[request.args.get('order_by')])
        else:
            sorted_questions_by_date = sorted(all_question, key=lambda i: i[request.args.get('order_by')],
                                              reverse=True)

    else:
        sorted_questions_by_date = sorted(all_question, key=lambda i: i['submission_time'])
    return render_template("question_list.html", all_question=sorted_questions_by_date,
                           header=data_handler.QUESTIONS_HEADER)


@app.route("/question/<question_id>")
def question(question_id):
    question_by_id = data_handler.get_questions_by_id(question_id, data_handler.QUESTION_FILE)
    all_answer = data_handler.get_all_answer()
    sorted_answer_by_vote = sorted(all_answer, key=lambda i: i['vote_number'])
    return render_template("answer_list.html", question=question_by_id, header=data_handler.ANSWERS_HEADER,
                           all_answer=sorted_answer_by_vote)


@app.route('/add_new_question', methods=['POST', 'GET'])
def add_new_question():
    if request.files:
        print('van file')
    # id,submission_time,view_number,vote_number,title,message,image
    if request.method == 'POST':
        new_question_data = data_handler.create_question_form(request.form.values())
        connection.append_csv_file(data_handler.QUESTION_FILE, new_question_data)
        if 'file' not in request.files:  # todo IMAGE!
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and data_handler.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
    return redirect("/")


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    all_answer = data_handler.get_all_answer()
    connection.write_csv_file(data_handler.ANSWER_FILE, all_answer, data_handler.ANSWERS_HEADER, answer_id)
    return redirect('/')


@app.route('/question/<question_id>/vote-up')
def vote_up_question(question_id):
    question_vote_up = data_handler.vote_up_question(question_id, data_handler.QUESTION_FILE)
    connection.write_csv(data_handler.QUESTION_FILE, question_vote_up, data_handler.QUESTIONS_HEADER, question_id)

    return redirect('/')


@app.route('/question/<question_id>/vote-down')
def vote_down_question(question_id):
    question_vote_down = data_handler.vote_down_question(question_id, data_handler.QUESTION_FILE)
    connection.write_csv(data_handler.QUESTION_FILE, question_vote_down, data_handler.QUESTIONS_HEADER, question_id)
    return redirect('/')


@app.route('/question/<question_id>/edit', methods=['POST', 'GET'])
def edit_question(question_id):
    question_by_id = data_handler.get_questions_by_id(question_id, data_handler.QUESTION_FILE)
    if request.method == 'POST':
        edited_question_data = data_handler.edit_question(request.form.items(), question_id)
        all_question = data_handler.get_all_question()
        connection.write_csv_file(data_handler.QUESTION_FILE, all_question, data_handler.QUESTIONS_HEADER, question_id)
        connection.append_csv_file(data_handler.QUESTION_FILE, edited_question_data.values())
        return redirect("/question/" + question_id)
    return render_template("edit_question.html", question_id=question_id, message=question_by_id['message'],
                           title=question_by_id['title'])


@app.route('/speak', methods=['POST', 'GET'])
def speak():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak")
        audio = r.listen(source, timeout=100.0, phrase_time_limit=100.0)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            if "dog" in text:
                if "title" in text:
                    return render_template("add_new_answer.html")
        except:
            print("sorry")

    return redirect('/')


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True, )
