import os
import datetime
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

number_str = []

path = 'main_2.log'
def logger(old_function):
    def new_function(*args, **kwargs):

        print(f'\nНазвание функции: {old_function.__name__}.'
              f'\nАргументы:{*args,}')

        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        result = old_function(*args, **kwargs)

        print(result)

        with open(path, 'a+', encoding='utf-8') as f:
                f.write(f'{now} \nНазвание функции: {old_function.__name__} \nАргуметы: {*args,} {kwargs}\nФункция возвращает {result}\n')
        return result
    return new_function


def del_duplicate(contacts_list):
    for i in range(len(contacts_list)):
        for j in range(i + 1, len(contacts_list)):
            if contacts_list[i][:2] == contacts_list[j][:2]:
                #print(i, j)
                number_str.append(j)
                for k in range(0, 7):
                    if contacts_list[i][k] == '':
                        contacts_list[i][k] = contacts_list[j][k]
    number_str.sort(reverse=True)
    #print(number_str)
    for ind in number_str:
        #print(ind)
        contacts_list.pop(ind)
    print(contacts_list)
    return contacts_list

@logger
def separate_fio(contacts_list):
    for rows in contacts_list:
        larst_name = [x for x in rows[0].split()]
        fio = [larst_name[i: i + 1] for i in range(0, len(larst_name), 1)]
        # print(fio)
        if len(fio) == 1:
            rows[0] = ''.join(fio[0])
        if len(fio) == 2:
            rows[0], rows[1] = ''.join(fio[0]), ''.join(fio[1])
        if len(fio) == 3:
            rows[0], rows[1], rows[2] = ''.join(fio[0]), ''.join(fio[1]), ''.join(fio[2])

        firstname = [x for x in rows[1].split()]
        io = [firstname[i: i + 1] for i in range(0, len(firstname), 1)]
        if len(io) == 1:
            rows[1] = ''.join(io[0])
        if len(io) == 2:
            rows[1], rows[2] = ''.join(io[0]), ''.join(io[1])
        # print(rows)

        pattern = r"(\+7|8)\s*\(*(\d+)[\)|-]*\s*(\d+)[\s|-]*(\d+)[\s|-]*(\d+)(\s*\(*(доб.)\s*(\d+)\)*)*"
        rows[5] = re.sub(pattern, r"+7\2\3\4\5 \7\8", rows[5])

        pattern = r"(\+7)(\d+)(\d+)(\d+)(\d+)(\d+)(\d+)(\d+)(\d+)"
        rows[5] = re.sub(pattern, r"+7(\2)\3\4\5-\6\7-\8\9", rows[5])
        


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        #pprint(contacts_list)

    separate_fio(contacts_list)
    del_duplicate(contacts_list)

    # TODO 2: сохраните получившиеся данные в другой файл
    # код для записи файла в формате CSV
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(contacts_list)