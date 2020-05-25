import csv


def get_answers():
    try:
        with open("answer.csv", "r") as file:
            reader = csv.DictReader(file)
            return [item for item in reader]
    except FileNotFoundError:
        return []

def get_all_question():
    try:
        with open('question.csv') as csv_file:
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

def find_answer_by_id(id):
    answer = get_answers()
    for dic in answer:
        if id in dic:
            return dic

#print(get_answers())

#print(get_all_question())
