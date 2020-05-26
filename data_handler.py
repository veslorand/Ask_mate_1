import csv
import os
import connection

DATA_FOLDER_PATH = os.getenv('DATA_FOLDER_PATH') if 'DATA_FOLDER_PATH' in os.environ else './'
QUESTION_FILE = DATA_FOLDER_PATH + "question.csv"



def get_questions_by_id(id, file_name):
    question = connection.read_csv_file(file_name)
    for dic in question:
        if id in dic:
            return dic



def get_all_question():
#    print(QUESTION_FILE)
#    try:
#        with open(QUESTION_FILE) as csv_file:
#            csv_reader = csv.DictReader(csv_file)
#            return [item for item in csv_reader]
#    except FileNotFoundError:
#        print("except")
#        return []


def find_answer_by_id(id, file_name):
     answer = connection.read_csv_file(file_name)
     for dic in answer:
         if id in dic:
             return dic

#print(get_answers())

#print(get_all_question())
