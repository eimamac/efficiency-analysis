import csv
from datetime import datetime
import os

import day
import day_case


def prepare_csv(csv_file):
    # add hours to empty gaps cuz its easier to analyze
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    last_hour = None
    for row in data:
        if row[1] == '':
            row[1] = last_hour
        else:
            last_hour = row[1]
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def readcsv():
    journal_csv = './journal.csv'
    prepare_csv(journal_csv)

    daycase = day_case.DayCase()
    journal_obj = csv.reader(open(journal_csv, "r", encoding='unicode_escape'))

    all_lines = []
    for line in journal_obj:
        all_lines.append(line)

    no_of_dates = 0
    cut_line = 0

    for line in all_lines:
        line_index = all_lines.index(line)
        if line[0] != '':
            no_of_dates += 1
        if no_of_dates == 2:
            no_of_dates = 1
            one_day_array = all_lines[cut_line:line_index]
            cut_line = line_index
            day1 = day.Day(one_day_array)
            daycase.add_day(day1)

        if line_index == len(all_lines) - 1:
            one_day_array = all_lines[cut_line:line_index + 1]
            day1 = day.Day(one_day_array)
            daycase.add_day(day1)
            # print('LAST day-------')
            # for i in one_day_array:
            #     print(i)

    return daycase