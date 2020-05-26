import csv
import os
import connection

DATA_FOLDER_PATH = os.getenv('DATA_FOLDER_PATH') if 'DATA_FOLDER_PATH' in os.environ else './'
QUESTION_FILE = DATA_FOLDER_PATH + "question.csv"
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def get_questions_by_id(id, file_name):
    question = connection.read_csv_file(file_name)
    for dic in question:
        if id in dic:
            return dic


def get_all_question():
    try:
        return connection.read_csv_file(QUESTION_FILE)
    except FileNotFoundError:
        print("except")
        return []


def find_answer_by_id(id, file_name):
    answer = connection.read_csv_file(file_name)
    for dic in answer:
        if id in dic:
            return dic

