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


def append_csv_file(file_name, new_question, header):
    with open(file_name, "a") as file:
        writer = csv.writer(file)
        writer.writerow(new_question)
