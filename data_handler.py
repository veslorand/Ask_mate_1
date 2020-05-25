import csv

def get_questions():
    question_list = []
    with open("question.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            question_list.append(row)
    return question_list

def get_answers():
    answer_list = []
    with open("answer.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            answer_list.append(row)
    return answer_list

def get_all_question():
    try:
        with open('/home/veslorandpc/Desktop/projects/Ask_mate_1/question.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            return [item for item in csv_reader]
    except FileNotFoundError:
        print("except")
        return []


print(get_all_question())
