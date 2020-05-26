import csv
import os


def read_csv_file(file_name):
    csv_item_list = []
    try:
        with open(file_name, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                csv_item_list.append(row)
        return csv_item_list
    except FileNotFoundError:
        return []


def write_csv_file(file_name, add_new):
    with open(file_name, "w") as file:
        for row in add_new:
            new_item = "".join(row)
            file.write(new_item)

