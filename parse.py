import xlrd
from bd import *

def parse_teacher(sheet):
    schedule = []
    for i in range(6):
        schedule.append([''] * 12)
    day = -1
    skip = 0
    teacher = sheet.cell_value(0, 0)
    for i in range(3, sheet.nrows):
        if skip > 0:
            skip -= 1
            continue
        day += 1
        presence = False
        for lesson in range(1, 13):
            if sheet.cell_value(i, lesson) == '':
                if not presence:
                    schedule[day][lesson - 1] = 'is not here yet'
                else:
                    schedule[day][lesson - 1] = 'free'
            else:
                presence = True
                schedule[day][lesson - 1] = sheet.cell_value(i + 3, lesson)
        if not presence:
            skip = 2
            for lesson in range(12):
                schedule[day][lesson] = 'absent'
        else:
            skip = 3
    res = (teacher, schedule)
    return res


def check(name):
    file = xlrd.open_workbook(name)
    for sheet in file.sheets():
        teacher, schedule = parse_teacher(sheet)
        print(teacher, schedule, sep='\n')
        for day in range(6):
            tmp = ''
            for i in schedule[day]:
                tmp += ", '" + i + "'"
            change(f"INSERT d{day+1}(buttons, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11) VALUES ({teacher}, {tmp})")
            print(f"INSERT d{day+1}(buttons, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11) VALUES ('{teacher}'{tmp});")