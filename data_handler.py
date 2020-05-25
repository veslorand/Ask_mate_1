import csv


def get_questions_by_id(id):
    question_list = []
    with open("question.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if id == row[0]:
                question_list.append(row)
    return question_list


def get_answer_by_id(id):
    question_list = []
    with open("question.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if id == row[0]:
                question_list.append(row)
    return question_list


def get_all_question():
    try:
        with open('question.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            return [item for item in csv_reader]
    except FileNotFoundError:
        print("except")
        return []


print(get_all_question())
