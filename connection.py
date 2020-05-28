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
        print(new_question)


def write_csv_file(file_name, dict_list, fieldnames, id):
    with open(file_name, "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for dictionary in dict_list:
            if dictionary['id'] == id:
                continue
            else:
                writer.writerow(dictionary)


# def edit_csv_file(file_name, question_id, all_question):
#     modded_file = []
#     with open(file_name) as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             if row.keys() == question_id:
#                 pass


def write_csv(file_name, to_change, fieldnames, question_id):
    questions = read_csv_file(file_name)
    for dict in questions:
        if question_id == dict['id']:
            questions.remove(dict)
            questions.append(to_change)
            break
    with open(file_name, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for dic in questions:
            writer.writerow(dic)


