import speech_recognition as sr
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

import connection
import data_handler
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/home/veslorandpc/Desktop/projects/Ask_mate_1/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
@app.route("/list")
def list_questions():
    all_question = data_handler.get_all_question()
    sorted_questions = connection.sort_the_questions(all_question, request.args.get('order_by'),
                                                     request.args.get('order_direction'))
    return render_template("question_list.html", all_question=sorted_questions,
                           header=data_handler.QUESTIONS_HEADER)


@app.route("/question/<question_id>")
def question(question_id):
    question_by_id = data_handler.get_questions_by_id(question_id, data_handler.QUESTION_FILE)
    all_answer = data_handler.get_all_answer()
    sorted_answer_by_vote = sorted(all_answer, key=lambda i: i['vote_number'], reverse=True)
    return render_template("answer_list.html", question=question_by_id, header=data_handler.ANSWERS_HEADER,
                           all_answer=sorted_answer_by_vote)


@app.route('/add_new_question', methods=['POST', 'GET'])
def add_new_question():
    # id,submission_time,view_number,vote_number,title,message,image
    if request.method == 'POST':
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
        new_question_data = data_handler.create_question_form(request.form.values(), filename)
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
    all_answer = data_handler.get_all_answer()
    connection.write_csv_file(data_handler.ANSWER_FILE, all_answer, data_handler.ANSWERS_HEADER, question_id)
    return redirect("/")


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    all_answer = data_handler.get_all_answer()
    connection.write_csv_file(data_handler.ANSWER_FILE, all_answer, data_handler.ANSWERS_HEADER, answer_id)
    return redirect('/')#f'/question/{all_answer["question_id"]}')


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


@app.route('/answer/<answer_id>/vote-up')
def vote_up_answer(answer_id):
    answer_vote_up = data_handler.vote_up_answer(answer_id, data_handler.ANSWER_FILE)
    connection.write_csv(data_handler.ANSWER_FILE, answer_vote_up, data_handler.ANSWERS_HEADER, answer_id)
    return redirect(f'/question/{answer_vote_up["question_id"]}')


@app.route('/answer/<answer_id>/vote-down')
def vote_down_answer(answer_id):
    answer_vote_down = data_handler.vote_down_answer(answer_id, data_handler.ANSWER_FILE)
    connection.write_csv(data_handler.ANSWER_FILE, answer_vote_down, data_handler.ANSWERS_HEADER, answer_id)
    return redirect(f'/question/{answer_vote_down["question_id"]}')


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
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak my Lord!")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5.0, phrase_time_limit=20.0)
            try:
                text = r.recognize_google(audio)  # language="hu-HU"
                print(f"You said: {text}")

                if "home" in text:                                                              # IN Everywhere
                    return redirect(url_for("list_questions"))                                  # TO Home
                elif "sort" in text:
                    print("sort")
                    if "time" in text:
                        if "descending" in text:
                            return redirect("http://0.0.0.0:8000/list?order_direction=desc&order_by=submission_time")
                        else:
                            return redirect("http://0.0.0.0:8000/list?order_direction=asc&order_by=submission_time")
                    if "view" in text:
                        if "descending" in text:
                            return redirect("http://0.0.0.0:8000/list?order_direction=desc&order_by=view_number")
                        else:
                            return redirect("http://0.0.0.0:8000/list?order_direction=asc&order_by=view_number")
                    if "vote" in text:
                        if "descending" in text:
                            return redirect("http://0.0.0.0:8000/list?order_direction=desc&order_by=vote_number")
                        else:
                            return redirect("http://0.0.0.0:8000/list?order_direction=asc&order_by=vote_number")
                    if "title" in text:
                        if "descending" in text:
                            return redirect("http://0.0.0.0:8000/list?order_direction=desc&order_by=title")
                        else:
                            return redirect("http://0.0.0.0:8000/list?order_direction=asc&order_by=title")
                    if "message" in text:
                        if "descending" in text:
                            return redirect("http://0.0.0.0:8000/list?order_direction=desc&order_by=message")
                        else:
                            return redirect("http://0.0.0.0:8000/list?order_direction=asc&order_by=message")

                elif "question" in text:                                                    # IN Everywhere
                    return redirect(url_for("add_new_question"))                                # TO Home

                elif request.environ['HTTP_REFERER'] in "http://0.0.0.0:8000/add_new_question": # IN Add new question
                    if "back" in text:                                                          # TO Back to Home
                        return redirect(url_for("list_questions"))

                elif "new-answer" in request.environ['HTTP_REFERER']:                           # IN New answer
                    if "back" in text:                                                          # TO Back question
                        return redirect(request.environ['HTTP_REFERER'][:-11])

                elif "question" in request.environ['HTTP_REFERER']:         # IN Question
                    if "answer" in text:                                                           # TO New answer
                        return redirect(request.environ['HTTP_REFERER'] + "/new-answer")


                print("Szeva")
                return redirect('/')
            except:
                print("Sorry i didn't understand it my Lord!")
                return redirect('/')
    except:
        return redirect('/')


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True, )
