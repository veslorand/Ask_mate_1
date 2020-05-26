import datetime
import os
import uuid

import connection

DATA_FOLDER_PATH = os.getenv('DATA_FOLDER_PATH') if 'DATA_FOLDER_PATH' in os.environ else './'
QUESTION_FILE = DATA_FOLDER_PATH + "question.csv"
ANSWER_FILE = DATA_FOLDER_PATH + "answer.csv"
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
QUESTION_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_questions_by_id(id, file_name):
    question = connection.read_csv_file(file_name)
    for dic in question:
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
        if id in dic:
            return dic


def get_random_id():
    return str(uuid.uuid4())


def get_date_time():
    time = datetime.datetime.now()
    return str(time)


def create_question_form(generator):
    my_list = [get_random_id(), get_date_time(), '0', '0', '']
    title_and_message = [i for i in generator]
    for ins in title_and_message[::-1]:
        my_list.insert(4, ins)
    return my_list
