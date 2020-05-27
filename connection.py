import csv


def read_csv_file(file_name):
    csv_item_list = []
    try:
        with open(file_name) as file:
            reader = csv.DictReader(file)
            for row in reader:
                csv_item_list.append(row)
        return csv_item_list
    except FileNotFoundError:
        return []


def append_csv_file(file_name, new_question):
    with open(file_name, "a") as file:
        writer = csv.writer(file)
        writer.writerow(new_question)


def write_csv_file(file_name, dict_list, fieldnames, id):
    with open(file_name, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for dictionary in dict_list:
            if dictionary['id'] == id:
                continue
            else:
                writer.writerow(dictionary)

def write_csv(file_name, to_change, question_id):
    questions = read_csv_file(file_name)
    for dict in questions:
        if question_id in dict:
            dict = to_change
    with open(file_name, "w") as file:
        writer = csv.DictWriter(file)
        writer.writeheader()
        writer.writerow(questions)


