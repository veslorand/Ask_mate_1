import csv
import os

DATA_FOLDER_PATH = os.getenv('DATA_FOLDER_PATH') if 'DATA_FOLDER_PATH' in os.environ else './'
QUESTION_FILE = DATA_FOLDER_PATH + "question.csv"



def get_questions_by_id(id):
    question_list = []
    with open(QUESTION_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if id == row[0]:
                question_list.append(row)
    return question_list


def get_answer_by_id(id):
    question_list = []
    with open(QUESTION_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if id == row[0]:
                question_list.append(row)
    return question_list


def get_all_question():
    print(QUESTION_FILE)
    try:
        with open(QUESTION_FILE) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            return [item for item in csv_reader]
    except FileNotFoundError:
        print("except")
        return []



def find_question_by_id(id):
    question = get_all_question()
    for dic in question:
        if id in dic:
            return dic


# def find_answer_by_id(id):
#     answer = get_answers()
#     for dic in answer:
#         if id in dic:
#             return dic

#print(get_answers())

#print(get_all_question())
