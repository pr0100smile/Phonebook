from pprint import pprint
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)

def correct_name(rows):
    corrections = [' '.join(worker[0:3]).split(' ')[0:3] + worker[3:7] for worker in rows]
    return corrections

def delete_dublication(final_list):
    without_copy = []
    for similar in final_list:
        for worker in final_list:
            if similar[0:2] == worker[0:2]:
                list_worker = similar
                similar = list_worker[0:2]
                for n in range(2, 7):
                    if list_worker[n] == '':
                        similar.append(worker[n])
                    else:
                        similar.append(list_worker[n])
        if similar not in without_copy:
            without_copy.append(similar)

    return without_copy

def correct_phone(rows, reg, corrections):
    phonebook_new = []
    pattern = re.compile(reg)
    phonebook_new = [[pattern.sub(corrections, string) for string in strings] for strings in rows]

    return phonebook_new


final_list = correct_name(contacts_list)
no_copy_list = delete_dublication(final_list)
reg = r'(\+7|8)+[\s(]*(\d{3,3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})'
correct_list = correct_phone(no_copy_list, reg, r'+7(\2)\3-\4-\5')
reg_2 = r'(\+7|8)+[\s(]*(\d{3,3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\s]*[(доб.\s]*(\d+)[)]*'
phonebook_new = correct_phone(correct_list, reg_2, r'+7(\2)\3-\4-\5 доб.\6')


with open("new_phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(phonebook_new)