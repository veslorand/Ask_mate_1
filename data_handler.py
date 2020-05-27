import datetime
import os
import uuid

import connection

DATA_FOLDER_PATH = os.getenv('DATA_FOLDER_PATH') if 'DATA_FOLDER_PATH' in os.environ else './'
QUESTION_FILE = DATA_FOLDER_PATH + "question.csv"
ANSWER_FILE = DATA_FOLDER_PATH + "answer.csv"
QUESTIONS_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWERS_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_questions_by_id(id, file_name):
    print(id)
    question = connection.read_csv_file(file_name)

    for dic in question:
        print(dic)
        if id == dic['id']:
            return dic


def get_all_question():
    try:
        return connection.read_csv_file(QUESTION_FILE)
    except FileNotFoundError:
        print("except")
        return []


def get_all_answer():
    try:
        return connection.read_csv_file(ANSWER_FILE)
    except FileNotFoundError:
        print("except")
        return []


def find_answer_by_id(id, file_name):
    answer = connection.read_csv_file(file_name)
    for dic in answer:
        if id in dic['id']:
            return dic


def get_random_id():
    return str(uuid.uuid4())


def get_date_time():
    time = datetime.datetime.now()
    return str(time)


def create_question_form(
        generator):  # 'id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image'
    my_list = [get_random_id(), get_date_time(), '0', '0', '']
    title_and_message = [i for i in generator]
    for ins in title_and_message[::-1]:
        my_list.insert(4, ins)
    return my_list


def create_answer_form(generator, question_id):  # 'id', 'submission_time', 'vote_number', 'question_id', 'message', 'image'
    my_list = [get_random_id(), get_date_time(), '0', question_id, '']
    title_and_message = [i for i in generator]
    for ins in title_and_message:
        my_list.insert(4, ins)
    return my_list


def edit_question(generator, question_id):
    question_by_id = get_questions_by_id(question_id, QUESTION_FILE)
    print(question_by_id)
    for dictionary in generator:
        print(question_by_id['title'])
        print(dictionary[0], dictionary[1])
        question_by_id['title'] = dictionary[1]
        if dictionary == question_id:
            question_by_id.update(4, dictionary['title'])
        elif dictionary[1] == 'message':
            question_by_id.update(5, dictionary['id'])
    print(question_by_id)
    return question_by_id


def vote_up(question_id, file_name):
    question_dict = get_questions_by_id(question_id, file_name)
    for item in question_dict.items():
        if item[0] == "vote_number":
            item[1] = int(item[1]) + 1
    return question_dict



