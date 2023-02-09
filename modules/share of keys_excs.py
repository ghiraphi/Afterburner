#программа для подсчёта количества исключений на один ключ
# -*- coding: utf-8 -*-
import re
from collections.abc import Iterable
from multiprocessing import Pool
import time
from collections import Counter
import datetime
def file(link):
    original_list_key=[]
    with open(link, 'r', encoding='utf-8-sig') as file_for_record:
        for line_for_original_list in file_for_record:
            line_for_original_list=(line_for_original_list.lower()).rstrip()
            original_list_key.append(line_for_original_list)
    return original_list_key
def repreg(base_line):
    #print('000', base_line)
    counter_num_orig_line = 0
    new_list_for_line = []
    global substring
    counter_num_orig_line += 1
    # программа меняет регулярки на спецсимволы. на входе строка с регуляркой. на выходе список строк без регулярок, на входе a - '(под|пере)жар* картошку' - на выходе a - ['поджар* картошку', 'пережар* картошку']
    base_line = base_line.replace('[а-я]+', '.*').replace('[0-9]+', '.*').replace('[1-9]+', '.*').replace('+', '').replace('[a-z]', '.').replace('[а-яa-z]', '.').replace('[a-zа-я]', '.').replace('[^а-я]', '£').replace('[1-9]', '£').replace('[0-9]', '£').replace('&#091', '©091').replace('&#093', '©093').replace('&#092', '©092').replace('&#047', '©047').replace('&#094', '©094').replace('&#036', '©036').replace('&#046', '©046').replace(
        '&#124', '©124').replace('&#063', '©063').replace('&#042', '©042').replace('&#043', '©043').replace('&#040', '©040').replace('&#041', '©041').replace('&#123', '©123').replace('&#125', '©125').replace('&#821', '©821').replace('&#061', '©061').replace('&#182', '©182')  # замена регулярок на звёздочки и точки
    # программа раскрывает квадратные скобки по выбранному диапозону. (0|1|2|3) вместо [0-3]
    p1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    p2 = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    if re.fullmatch('.*\[\w\-\w\].*', base_line):
        num = len(re.findall('\[\w\-\w\]', base_line))  # количество квадратных скобок с '-'
        for i in range(num):  # замена квадратных скобко и букв на варианты круглых скобок
            dl = len(base_line)  # количество букв в элементе
            for k in range(dl):  # в диапозоне количества букв
                if base_line[k] == '[' and base_line[k + 2] == '-':
                    if base_line[k + 1] in p1:
                        s_o = p1.index(base_line[k + 1])
                    if base_line[k + 1] in p2:
                        s_o = p2.index(base_line[k + 1])
                    start = k  # начальная позиция квадратной скобки
                if base_line[k] == ']' and base_line[k - 2] == '-':
                    if base_line[k - 1] in p1:
                        s_f = p1.index(base_line[k - 1])
                    if base_line[k - 1] in p2:
                        s_f = p2.index(base_line[k - 1])
                    end = k  # финальная позиция квадратной скобки
                    break
            if base_line[k - 1] in p1:  # если это цифра
                p = '|'.join(p1[s_o:s_f + 1])  # добавляем в указанное перечисление цифр этой скобки слэши
            if base_line[k - 1] in p2:  # если это буква
                p = '|'.join(p2[s_o:s_f + 1])  # добавляем в указанное перечисление букв  этой скобки слэши
            base_line = base_line[:start] + '(' + p + ')' + base_line[end + 1:]  # преобразовываем квадратные скобки в круглые. становится основным выражением.
            # дальше по кругу

    # программа рабоатет с выражением [^x], раскрывает и выдаёт полную скобку за исключением символа x
    if re.findall('.*\[\^.*', base_line):
        p0 = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы',
              'ь', 'э', 'ю', 'я', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # символы, которые используются в [^x]
        y = 0
        num = len(re.findall('\^', base_line))  # количество квадратных скобок с '^'
        base_line = base_line.split(' ', 0)  # сделай из изначальной строки список с одним элементом
        schetchik = 0
        for s in base_line:
            dl = len(s)  # количество букв в элементе
            for k in range(dl):  # в диапозоне количества букв
                if s[k] == '^' and y == 0:  # высчитывает, откуда начинается скобка и где заканчивается
                    start = k + 1
                    y = y + 1
                if s[k] == ']' and y == 1:
                    end = k
                    y = y - 1
                    break
            x = s[int(start):int(end)]  # все буквы-цифры , которые не должны учитываться
            vrem = []
            for i in x:  # перебирает все символы в скобке
                isk = p0.index(i)  # находит индекс в списке, чтобы потом исключить его
                p = p0[:isk] + p0[isk + 1:]  # собирает скобку без учёта указанных символов
                vrem.append(p)  # добавляет во временный список
            vrem = '(' + '|'.join(list(set.intersection(*map(set, vrem)))) + ')'  # собирает готовую скобку
            s = s[:start - 2] + vrem + s[end + 1:]  # собирает готовое выражение, строку
            base_line.append(s)  # добавляет в текущий список
            schetchik = schetchik + 1
            if schetchik != num:  # прекращает работать, если проверил все значения
                continue
            else:
                break
        base_line = [i for i in base_line if '^' not in i]  # выбирает значения только без ^
        base_line = ''.join(base_line)

    # программа заменяет квадратные скобки и буквы в них на варианты круглых скобок
    #base_line = re.sub(' \d,\d+ ', ' ', base_line)  # убираем расстояния, делаем так, будто их не было
    base_line = base_line.replace(',', '®')
    num = len(re.findall('\[', base_line))  # количество квадратных скобок
    num2 = len(re.findall('\[\^', base_line))  # количество квадратных скобок исключений
    num = num - num2  # вычитаем разницу, чтобы считать нужное число вариантов
    r = 0
    for i in range(num):  # замена квадратных скобко и букв на варианты круглых скобок
        dl = len(base_line)  # количество букв в элементе
        for k in range(dl):  # в диапозоне количества букв
            if base_line[k] == '[' and base_line[k + 2] != '-' and base_line[k + 1] != '^':
                start = k  # начальная позиция квадратной скобки
                r = r + 1
            if base_line[k] == '[' and base_line[k + 1] == '^':
                continue
            if base_line[k] == '[' and base_line[k + 2] == '-':
                continue
            if base_line[k] == ']' and base_line[k - 2] != '-' and r == 1:
                end = k  # финальная позиция квадратной скобки
                r = r - 1
                break
        p = base_line[start + 1:end]  # участок квадратной скобки
        p = '|'.join(p)  # добавляем между буквами в этой скобки слэши
        base_line = base_line[:start] + '(' + p + ')' + base_line[end + 1:]  # преобразовываем квадратные скобки в круглые. становится основным выражением.  дальше по кругу


    # программа раскрывает фигурные скобки и даёт все значения согласно {x}
    base_line = base_line.split(' ', 0)  # сделай из изначальной строки список с одним элементом
    for str_ss in base_line:  # итерация по списку строк
        if '{' in str_ss:  # если в строке есть круглая скобка
            for kes in range(len(str_ss)):  # пройдись по каждому элементу строки. по каждой букве
                if str_ss[kes] == '{':  # если есть открыв.скобка
                    t1 = kes  # назначь индекс этой скобке
                if str_ss[kes] == '}':  # если есть открыв.скобка
                    t2 = kes  # назначь индекс этой скобке
                    if re.search('®', str_ss[t1 + 1:t2]):  # в этих круглых скобках есть диапозон?
                        start_finish = str_ss[t1 + 1:t2].split('®')
                        start_f1 = round(float(start_finish[0]))
                        finish_f1 = round(float(start_finish[1]))
                        len_sumok = finish_f1 - start_f1  # знай сколько вариантов в диапазоне
                    else:
                        start_finish = [(str_ss[t1 + 1:t2]), (str_ss[t1 + 1:t2])]
                        start_f1 = round(float(start_finish[0]))
                        finish_f1 = round(float(start_finish[1]))
                    break
            nvs = []  # временный список для добавления новых значений
            for dnkz in range(start_f1, (finish_f1) + 1):  # в диапозоне начального и конечного значения
                if str_ss[t1 - 1] != ')' and str_ss[t1 - 1] != ']':
                    nvs.append(str_ss[:t1 - 1] + str_ss[t1 - 1] * dnkz + str_ss[t2 + 1:])  # добавь в новый список строки с учётом количества {
                if str_ss[t1 - 1] == ')':
                    for index, bukva in reversed(list(enumerate(str_ss[:t1]))):
                        if bukva == '(':
                            nvs.append(str_ss[:index] + str_ss[index:t1] * dnkz + str_ss[t2 + 1:])
                            break
                if str_ss[t1 - 1] == ']':
                    for index, bukva in reversed(list(enumerate(str_ss[:t1]))):
                        if bukva == '[':
                            nvs.append(str_ss[:index] + str_ss[index:t1] * dnkz + str_ss[t2 + 1:])
                            break
            [base_line.append(nvs_i) for nvs_i in nvs]  # добавь новые значения из временного в основной список
    base_line = [ai for ai in base_line if '{' not in ai]

    # программа убирает лишние скобки, которые не имели нагрузки
    for substring in base_line:
        substring = list(substring)  # строка меняется на элемент списка
        kn = len(substring)  # количество строк в списке
        predel = 0
        # определяет, где начинается старт и финиш - маскируя внутренние скобки со слешами, убирая пустые скобки , где нет слеша или знака вопрсоа
        while '(' in substring or ')' in substring or '|' in substring:  # пока есть слэши и скобки в списке
            predel += 1
            for k in range(0, kn):  # итерация по количеству букв в списке
                if re.fullmatch('\(', substring[k]) and re.fullmatch('\)', substring[k + 1]):  # если в строке есть скобка откр и закр ()
                    start = k  # фиксация начала
                    finish = k + 1  # фиксация конца
                    break
                if re.fullmatch('\(', substring[k]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\=|\?|@|<|\-|\*|\[|\]|\+|\.|#)', substring[k + 1]):  # если в строке скобка откр и дальше буква
                    start = k  # фиксация начала
                    continue
                if re.fullmatch('\)', substring[k]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\=|\?|@|>|\-|\*|\[|\]|\?|\+|\.|#)', substring[k - 1]):  # если в строке скобка закр  и перед этим буква
                    finish = k  # фиксация конца
                    break  # останавливай цикл, переходи к след
            dlskob = len(''.join(substring[start + 1:finish]))
            try:
                if '|' not in substring[start + 1:finish] and '(' not in substring[start + 1:finish] and ')' not in substring[start + 1:finish] and finish != dlskob + 1:  # если нет слэша внутри скобок , тогда
                    if '?' not in substring[finish + 1]:
                        substring[start] = '@'  # меняй скобки начала и конца на знак
                        substring[finish] = '@'
                if '|' not in substring[start + 1:finish] and '(' not in substring[start + 1:finish] and ')' not in substring[start + 1:finish] and '?' not in substring[finish] and finish == dlskob + 1:  # если нет слэша внутри скобок , тогда
                    substring[start] = '@'  # меняй скобки начала и конца на знак
                    substring[finish] = '@'
                if '|' not in substring[start + 1:finish] and '(' not in substring[start + 1:finish] and ')' not in substring[start + 1:finish] and '?' in substring[finish + 1] and dlskob >= 2:  # если нет слэша внутри скобок , тогда
                    substring[start] = '<'  # меняй скобки начала и конца на знак
                    substring[finish] = '>'
                if '|' not in substring[start + 1:finish] and '(' not in substring[start + 1:finish] and ')' not in substring[start + 1:finish] and '?' in substring[finish + 1] and dlskob == 1:  # если нет слэша внутри скобок , тогда
                    substring[start] = '@'  # меняй скобки начала и конца на знак
                    substring[finish] = '@'
                if '|' in substring[start + 1:finish]:  # если слэш между скобок
                    substring[start] = '<'  # меняй скобки начала и конца на знак
                    substring[finish] = '>'
                    spisok = []  # создай пустой список
                    for k, i in enumerate(substring[start + 1:finish]):  # итерация по внутренности скобки
                        if i == '|':  # есть если слэш
                            spisok.append(k)  # добавь в список индекс этого слэша
                    for i in range(len(spisok)):  # итерация по индексам слэшей
                        substring[start + 1 + spisok[i]] = '&'  # меняй слэш на знак, учитывая расстояние (индекс)
            except IndexError:
                if '|' not in substring[start + 1:finish] and '(' not in substring[start + 1:finish] and ')' not in substring[start + 1:finish] and finish != dlskob + 1:  # если нет слэша внутри скобок , тогда
                    substring[start] = '@'  # меняй скобки начала и конца на знак
                    substring[finish] = '@'
                if '|' not in substring[start + 1:finish] and '(' not in substring[start + 1:finish] and ')' not in substring[start + 1:finish] and '?' not in substring[finish] and finish == dlskob + 1:  # если нет слэша внутри скобок , тогда
                    substring[start] = '@'  # меняй скобки начала и конца на знак
                    substring[finish] = '@'
                if '|' in substring[start + 1:finish]:  # если слэш между скобок
                    substring[start] = '<'  # меняй скобки начала и конца на знак
                    substring[finish] = '>'
                    spisok = []  # создай пустой список
                    for k, i in enumerate(substring[start + 1:finish]):  # итерация по внутренности скобки
                        if i == '|':  # есть если слэш
                            spisok.append(k)  # добавь в список индекс этого слэша
                    for i in range(len(spisok)):  # итерация по индексам слэшей
                        substring[start + 1 + spisok[i]] = '&'  # меняй слэш на знак, учитывая расстояние (индекс)
            if predel > 100:
                substring = (''.join([k for k in substring]))  # подготавливаем из списка строку
                substring = list(substring.replace('@|@', '|').replace(' @', ' (').replace('@ ', ') '))
                if substring[0] == '@':
                    substring[0] = '('
                if substring[len(substring) - 1] == '@':
                    substring[len(substring) - 1] = ')'

    base_line = (''.join([k for k in substring if k != '@']))  # верни строку, не замечая знак @ - пустые скобки
    f = base_line.replace('<', '(').replace('>', ')').replace('&', '|')
    f = f.split(maxsplit=0)

    # программа раскрывает скобки со знаком '?' и делает все возможные варианты
    for x, i in enumerate(f):  # иетарция по элементам списка, где есть знак вопроса, так мы находим скобки , после которых стоит знак вопроса. означает - или да или нет.
        if ')?' in i:
            i = list(i)  # преобразуем строку в список. чтобы была итерация по буквам этой строки
            for k in range(len(i)):  # итерация по количеству букв в списке
                if re.fullmatch('\(', i[k]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|\-|\*|\[|\]|\.|\+|\|)', i[k + 1]):  # если в строке скобка
                    start = k  # фиксация начала скобки со знаком вопроса
                    continue
                if re.fullmatch('\(', i[k]) and re.fullmatch('\)', i[k + 1]) and re.fullmatch('\?', i[k + 2]):  # если есть выражение вида ()?, то сразу преобраует в спец символы, чтобы потом убирать эту строку
                    f[x] = '#$'
                    break
                try:
                    if re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\?|\.|@|&|<|>|\-|\*|\[|\]|\.|\+|\||\.)', i[k - 1]) and re.fullmatch('\)', i[k]) and re.fullmatch('(\|)', i[k + 1]):  # если есть выражение вида -   текст)|
                        i[k] = '>'  # преобразовывает в спец символ ближнюю скобку и слэши внутри, замораживая, чтобы программа думала, что это буквы и не обращала внимание на скобки и слэши
                        i[start] = '<'
                        otrezok = i[start + 1:k]
                        if '|' in otrezok:  # работа по заморозке слешей внутри скобки
                            spisok = []
                            for r in range(len(otrezok)):
                                if otrezok[r] == '|':
                                    spisok.append(r)
                            for y in range(len(spisok)):  # итерация по индексам слэшей
                                i[start + 1 + spisok[y]] = '&'  # меняй слэш на знак, учитывая расстояние (индекс)
                        f.append(''.join(i))
                        f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                        break
                    if re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\?|\.|@|&|<|>|\-|\*|\[|\]|\.|\+|\||\.)', i[k - 1]) and re.fullmatch('\)', i[k]) and re.fullmatch('\)', i[k + 1]) and re.fullmatch('\?', i[k + 2]):  # если есть выражение вида -  ( абв))?
                        i[k] = '>'  # преобразовывает в спец символ ближнюю скобку и слэши внутри, замораживая, чтобы программа думала, что это буквы и не обращала внимание на скобки и слэши
                        i[start] = '<'
                        otrezok = i[start + 1:k]
                        if '|' in otrezok:  # работа по заморозке слешей внутри скобки
                            spisok = []
                            for r in range(len(otrezok)):
                                if otrezok[r] == '|':
                                    spisok.append(r)
                            for y in range(len(spisok)):  # итерация по индексам слэшей
                                i[start + 1 + spisok[y]] = '&'  # меняй слэш на знак, учитывая расстояние (индекс)
                        f.append(''.join(i))
                        f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                        break
                    if re.fullmatch('(\|)', i[start - 1]) and re.fullmatch('\)', i[k]) and i[k + 1] != '?':  # если есть выражение вида -   текст)|
                        i[k] = '>'  # преобразовывает в спец символ ближнюю скобку и слэши внутри, замораживая, чтобы программа думала, что это буквы и не обращала внимание на скобки и слэши
                        i[start] = '<'
                        otrezok = i[start + 1:k]
                        if '|' in otrezok:  # работа по заморозке слешей внутри скобки
                            spisok = []
                            for r in range(len(otrezok)):
                                if otrezok[r] == '|':
                                    spisok.append(r)
                            for y in range(len(spisok)):  # итерация по индексам слэшей
                                i[start + 1 + spisok[y]] = '&'  # меняй слэш на знак, учитывая расстояние (индекс)
                        f.append(''.join(i))
                        f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                        break
                    if re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\?|\.|@|&|<|>|\-|\*|\[|\]|\.|\+|\||\.)', i[k - 1]) and re.fullmatch('\)', i[k]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\.|@|&|<|>|\-|\*|\[|\]|\.|\+|\||\.)', i[k + 1]):  # !!! тут был прецедент. стоял знак вопроса. я его убрал.   если есть выражение вида -   текст))
                        i[k] = '>'
                        i[start] = '<'
                        otrezok = i[start + 1:k]
                        if '|' in otrezok:
                            spisok = []
                            for r in range(len(otrezok)):
                                if otrezok[r] == '|':
                                    spisok.append(r)
                            for y in range(len(spisok)):  # итерация по индексам слэшей
                                i[start + 1 + spisok[y]] = '&'  # меняй слэш на знак, учитывая расстояние (индекс)
                        f.append(''.join(i))
                        f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                        break

                    if i[0] == '(' and start == 1 and re.fullmatch('\)', i[k]) and i[k + 1] != '?':  # если есть выражение вида -   текст)|
                        i[k] = '>'  # преобразовывает в спец символ ближнюю скобку и слэши внутри, замораживая, чтобы программа думала, что это буквы и не обращала внимание на скобки и слэши
                        i[start] = '<'
                        otrezok = i[start + 1:k]
                        if '|' in otrezok:  # работа по заморозке слешей внутри скобки
                            spisok = []
                            for r in range(len(otrezok)):
                                if otrezok[r] == '|':
                                    spisok.append(r)
                            for y in range(len(spisok)):  # итерация по индексам слэшей
                                i[start + 1 + spisok[y]] = '&'  # меняй слэш на знак, учитывая расстояние (индекс)
                        f.append(''.join(i))
                        f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                        break
                    if re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\?|\.|@|&|<|>|\-|\*|\[|\]|\.|\+|\||\.)', i[k - 1]) and re.fullmatch('\)', i[k]) and re.fullmatch('(\?)', i[k + 1]):  # если  выражение -   текст)? - дальше перечисляются все ситуации, чтобы раскрывать эти скобки
                        finish = k  # фиксация конца скобки со знаком вопроса
                        if ')' not in i[start + 1:finish] and '(' not in i[start + 1:finish]:
                            if '|' in i[start + 1:finish] and i[start - 1] != '|' and i[start - 1] != '(' and finish + 1 == len(i) - 1:  # 1.2.2.0
                                f.append(''.join(i[:start] + i[start:finish + 1] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                            if '|' in i[start + 1:finish] and i[start - 1] != '|' and i[start - 1] != '(' and i[finish + 2] != ' ':  # 1.1.1.0
                                f.append(''.join(i[:start] + i[start:finish + 1] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                            if '|' in i[start + 1:finish] and i[start - 1] != '|' and i[start - 1] != '(' and i[finish + 2] == ' ':  # 1.2.2.0
                                f.append(''.join(i[:start] + i[start:finish + 1] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break

                            if '|' in i[start + 1:finish] and i[start - 1] != '|' and i[start - 1] == '(' and i[finish + 2] != '|':  # 1.1.1
                                f.append(''.join(i[:start] + i[start:finish + 1] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                            if '|' in i[start + 1:finish] and i[start - 1] != '|' and i[start - 1] == '(' and i[finish + 2] == '|':  # 1.1.2
                                f.append(''.join(i[:start] + i[start:finish + 1] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 3:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break

                            if '|' not in i[start + 1:finish] and i[start - 1] == '|' and i[start - 2] == '(':  # 1.2.1
                                f.append(''.join(i[:start] + i[start + 1:finish] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start - 1] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                            if '|' not in i[start + 1:finish] and i[start - 1] == '|' and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\.|@|&|<|>|\-|\*|\[|\]|\+)', i[start - 2]) and i[finish + 2] == ')':  # 1.2.2.1
                                f.append(''.join(i[:start] + i[start + 1:finish] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start - 1] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                            if '|' not in i[start + 1:finish] and i[start - 1] == '|' and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\.|@|&|<|>|\-|\*|\[|\]|\+)', i[start - 2]) and i[finish + 2] == '|':  # 1.2.2.2
                                f.append(''.join(i[:start] + i[start + 1:finish] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 3:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                            if '|' not in i[start + 1:finish] and i[start - 1] == '|' and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\.|@|&|<|>|\-|\*|\[|\]|\+)', i[start - 2]) and re.fullmatch(
                                    '(\w|©|®|£|\{|\}|\%|\?|\.|@|&|<|>|\-|\*|\[|\]|\+)', i[finish + 2]):  # 1.2.2.3
                                f.append(''.join(i[:start] + i[start + 1:finish] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break

                                # дальше была одна скобка, но её  из-за длины и несовпадения (индекс выходил за пределы диапозона) пришлось размножить
                            if len(i) - 1 < finish + 2:  # если длина итеририруемого выражения меньше индекса элемента, то тогда проверяем ближайший элемент после )

                                if '|' not in i[start + 1:finish] and i[start - 1] != '|' and i[finish + 1] != '|':  # 1.3.1
                                    f.append(''.join(i[:start] + i[start + 1:finish]))  # добавь в общий список скобку, где есть знак вопроса
                                    f.append(''.join(i[:start]))  # добавь в общий список скобку, где нет знака вопроса
                                    f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                    break
                            if len(i) - 1 >= finish + 2:  # если длина итеририруемого выражения больше или равна индексу элемента, то тогда всё ок, проверяем дальний элемент после ) (финиша)

                                if '|' not in i[start + 1:finish] and i[start - 1] != '|' and i[finish + 2] != '|':  # 1.3.2
                                    f.append(''.join(i[:start] + i[start + 1:finish] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                    f.append(''.join(i[:start] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                    f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                    break

                            if '|' not in i[start + 1:finish] and i[start - 1] != '|' and i[finish + 2] == '|' and i[start - 1] == '(':  # 1.4.1
                                f.append(''.join(i[:start] + i[start + 1:finish] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 3:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                            if '|' not in i[start + 1:finish] and i[start - 1] != '|' and i[finish + 2] == '|' and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\.|@|&|<|>|\-|\*|\[|\]|\+)', i[start - 1]):  # 1.4.2
                                f.append(''.join(i[:start] + i[start + 1:finish] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break

                            if '|' in i[start + 1:finish] and i[start - 1] == '|':  # 1.5
                                f.append(''.join(i[:start] + i[start:finish + 1] + i[finish + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                                f.append(''.join(i[:start] + i[finish + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                                f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                                break
                except IndexError:
                    pass
            if re.search('\)\)\?', ''.join(i)) and re.search('\(\(', ''.join(i)):  # chebur
                for k in range(len(i)):  # итерация по количеству букв в списке
                    if re.fullmatch('\(', i[k - 1]) and re.fullmatch('\(', i[k]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|\-|\*|\[|\]|\.|\+|\|)', i[k + 2]):  # если в строке скобка ((а
                        start2 = k  # фиксация начала скобки со знаком вопроса
                        continue
                    if re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|\?|\.|@|&|<|>|\-|\*|\[|\]|\.|\+|\||\.)', i[k - 2]) and re.fullmatch('\)', i[k - 1]) and re.fullmatch('\)', i[k]) and re.fullmatch('(\?)', i[k + 1]):  # б))?
                        f.append(''.join(i[:start2] + i[start2 + 1:k] + i[k + 2:]))  # добавь в общий список скобку, где есть знак вопроса
                        f.append(''.join(i[:start2 - 1] + i[k + 2:]))  # добавь в общий список скобку, где нет знака вопроса
                        f[x] = '#$'  # замени обрабатываемую строку на эти символы, чтобы потом их скрыть
                        break
        base_line = (list(set([k for k in f if k != '#$'])))  # генерируем список, в котором нет обрабатываемых строк. через множество избавляемся от повторяющихся значений. создаём обратно список
        for x in range(len(base_line)):
            base_line[x] = base_line[x].replace('<', '(').replace('>', ')').replace('&', '|')  # возвращаем обратно скобки и слэши

    sl_zap = []
    for i in base_line:
        sl_zap.append(i.replace(',', '®'))
    base_line = sl_zap
    # программа раскрывает скобки и делает все возможны варианты
    base_line = ','.join(base_line)
    #print('008', base_line)
    esheodin = []
    while '|' in base_line:
        #print('007')
        spis_strok = base_line.split(',')
        spis_strok = list(set(spis_strok))
        for indexstr, stroka in enumerate(spis_strok):
            if '|' in stroka:
                #print(len(esheodin),  len(spis_strok) )
                if re.search('\(\S+ ', stroka):
                    while re.search('\(\S+ ', stroka) or re.search(' \S+\)', stroka) or re.search(' \S+\|', stroka) or re.search('\|\S+ ', stroka):
                        for bukva in range(len(stroka)):
                            if (re.fullmatch('\(', stroka[bukva])) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|>|\-|_|\?|\*|\[|\]|\.|\+|\|)', stroka[bukva + 1]):  # если в строке скобка
                                start = bukva  # фиксация начала скобки со знаком вопроса
                                continue
                            if (re.fullmatch('\)', stroka[bukva])) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|>|\-|_|\?|\*|\[|\]|\.|\+|\|)', stroka[bukva - 1]):  # если в строке скобка
                                end = bukva  # фиксация начала скобки со знаком вопроса
                                break
                        skobka = stroka[start:end + 1]
                        if re.search('\(\S+ ', skobka) or re.search(' \S+\)', skobka) or re.search(' \S+\|', skobka) or re.search('\|\S+ ', skobka):
                            skobka = skobka.replace(' ', '_').replace('(', '<').replace(')', '>').replace('|', '&')
                            stroka = stroka[:start] + skobka + stroka[end + 1:]
                        else:
                            skobka = skobka.replace('(', '<').replace(')', '>').replace('|', '&')
                            stroka = stroka[:start] + skobka + stroka[end + 1:]
                    stroka = stroka.replace('<', '(').replace('>', ')').replace('&', '|')
                spis_slov = stroka.split()
                for slovo in spis_slov:  # определяем кусок со скобкой
                    if re.match('\)\S*', slovo) or re.match('\S*\(', slovo):
                        slovo = list(slovo)
                        for bukva in range(len(slovo)):
                            if re.fullmatch('\(', slovo[bukva]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|>|\-|_|\?|\*|\[|\]|\.|\+|\|)', slovo[bukva + 1]):  # если в строке скобка
                                start = bukva  # фиксация начала скобки со знаком вопроса
                                continue
                            if re.fullmatch('\)', slovo[bukva]) and re.fullmatch('(\w|©|®|£|\{|\}|\%|\?|@|<|>|\-|_|\?|\*|\[|\]|\.|\+|\|)', slovo[bukva - 1]):  # если в строке скобка
                                end = bukva  # фиксация начала скобки со знаком вопроса
                                break
                        slovo = ''.join(slovo)
                        skobka = slovo[start:end + 1]
                        skobka = skobka.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace("'", '')
                        slova_v_skobke = skobka.split('|')  # сделали варианты внутри скобки. добавили в новый список
                        slova_v_skobke.insert(0, spis_slov.index(slovo))  # добавили индекс
                        kolvo_slov_v_skob = len(slova_v_skobke) - 1  # минусуем на один, потому что один из элементов - это индекс. а нам надо знать точно количество слов
                        break
                new_stroki_vmeste = []

                for nomer_slova_v_skob in range(0, kolvo_slov_v_skob):
                    new_stroka = []
                    for indexslova, slovo in enumerate(spis_slov):
                        if '|' not in slovo:
                            new_stroka.append(slovo)
                        if '|' in slovo:
                            if indexslova == slova_v_skobke[0]:
                                vrem1 = []
                                vrem1.append(slovo[:start])
                                vrem1.append(slova_v_skobke[nomer_slova_v_skob + 1])
                                vrem1.append(slovo[end + 1:])
                                new_stroka.append(''.join(vrem1))
                            else:
                                new_stroka.append(slovo)
                    new_stroki_vmeste.append(' '.join(new_stroka))
                for new_stroka_vmeste in new_stroki_vmeste:
                    new_stroka_vmeste = new_stroka_vmeste.replace('_', ' ')
                    if '|' not in new_stroka_vmeste:
                        esheodin.append(new_stroka_vmeste)
                        #print(len(esheodin), 'ещё один список')

                    else:
                        spis_strok.append(new_stroka_vmeste)
                        #print(len(spis_strok), '                             spis_strok')

                spis_strok[indexstr] = '$'
                spis_strok = list(set([k for k in spis_strok if k != '$']))
                break
        base_line = ','.join(spis_strok)
        if spis_strok==[]:
            base_line = list(set(esheodin))
    #print('0091', base_line, type(base_line))
    # программа перебирает все возможные варианты с одиночным знаком вопроса
    sp_bez_zn_vopr = []
    if type(base_line)==str:
        base_line=base_line.split(',')
    #print('0092', base_line, len(base_line))
    for nom_strok in range(len(base_line)):
        if '?' in base_line[nom_strok]:
            #print('==-=',base_line[nom_strok])
            ##print(a[nom_strok], 'a[nom_strok]')
            slovo = base_line[nom_strok]
            count = 0
            slovo = slovo.replace('((', '(').replace('))', ')').replace(')|(', '|')
            slovo = re.sub('^\(', '', slovo)
            slovo = re.sub('\)$', '', slovo)
            from itertools import permutations
            chet = []
            num_var = 2 ** len(re.findall("\?", slovo))  # количество вариатов перебора со знаком вопроса
            for k, e in enumerate(slovo):
                if e == '(':
                    chet.append(k)
                if e == ')':
                    chet.append(k)
            lend = len(chet)
            for i in range(0, lend - 1):
                if i % 2 == 0:
                    k = slovo[chet[i]:chet[i + 1] + 1].replace('(', '<').replace(')', '>').replace('|', '$')
                    slovo = slovo[:chet[i]] + k + slovo[chet[i + 1] + 1:]  # код ради того, чтобы правильно делить внутренние скобки
            if re.match('.*\?*', slovo):
                slovo = slovo.split('|')  # разбили строку на подстроки-слова по слэшу
                for i, j in enumerate(slovo):  # индекс слова. итерируем внутри каждого элемента между слэшами
                    if '?' in j:  # если в элементе есть знак вопроса, то
                        for k, p in enumerate(j):  # итерируем этот элемент между слэшами по буквам
                            if '?' in p:  # если '?' в букве, то
                                slovo.append(slovo[i][:k] + slovo[i][k + 1:])  # добавляем обработанные новые элементы в тек.список
                                slovo.append(slovo[i][:k - 1] + slovo[i][k + 1:])
                                slovo[i] = []  # делаем пустыми элементы, которые уже обработали
            name_var = list(filter(lambda x: x, slovo))  # итоговый варианты (список) со знаком "?" и без него.
            for i in name_var:
                sp_bez_zn_vopr.append(''.join(i))
        else:
            sp_bez_zn_vopr.append(base_line[nom_strok])
    new_list_from_original_line_key = list(set(sp_bez_zn_vopr))
    #print('010', new_list_from_original_line_key)
    return new_list_from_original_line_key
def compare_words(word_from_line_key, word_from_line_exc):
    fix_match_word_key_and_exc = 0
    # ключ - *абв* - ключ
    if word_from_line_key[0] == '*' and word_from_line_key[len(word_from_line_key) - 1] == '*':

        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - *а*бв* или *абв*
            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) == len(word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0

                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:len(word_from_line_key) - 1]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[1:len(word_from_line_exc) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da1')
                        break

            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) > len(word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key[1:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da2')
                        break  # искл - *а*бв* или *абв*   #искл - *а*бв* или *абв*

        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*':  # искл - *абв или *а*бв
            if len(word_from_line_exc[1:]) == len(word_from_line_key[1:len(word_from_line_key) - 1]) and word_from_line_key[len(word_from_line_key) - 2] == word_from_line_exc[
                len(word_from_line_exc) - 1]:  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:len(word_from_line_key) - 1]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[1:]):
                        fix_match_word_key_and_exc = 1
                        #print('da3')
                        break
            if len(word_from_line_exc[1:]) > len(word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key[1:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da4')
                        break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - абв*
            if len(word_from_line_exc[:len(word_from_line_key) - 1]) == len(word_from_line_key[1:len(word_from_line_key) - 1]) and word_from_line_key[1] == word_from_line_exc[0]:  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_key) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:len(word_from_line_key) - 1]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[:len(word_from_line_key) - 1]) - 1:
                        fix_match_word_key_and_exc = 1
                        #print('da5')
                        break
            if len(word_from_line_exc[:len(word_from_line_key) - 1]) > len(word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0

                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_exc)]))):  # проверка межзвёзднной части на совпадение
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                                ##print(num, '+++num')
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key[1:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da6')
                        break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc) == None:  # искл - слово без звёзд. обычное слово
            ##print(line_exc, 'искл - слово без звёзд. обычное слово2')
            sind = 0

            while fix_match_word_key_and_exc != 1:

                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                ##print('while prov != 1')
                for index_letter_key, letter_key in (list(enumerate(word_from_line_key[1:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in (list(enumerate(word_from_line_exc))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc + 1 and index_letter_key == fix_index_letter_key + 1):

                            if (letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key))):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                        if counter_match == len(word_from_line_key[1:len(word_from_line_key) - 1]):
                            fix_match_word_key_and_exc = 1
                            #print('da7')
                            break

                if fix_match_word_key_and_exc != 1:
                    ##print('точно нет совпадений между *ключом* и простым исклом')
                    break

                #     sind += 1
                #
                # if sind == len(line_exc) :
                #     ##print(sind,  len(line_exc) - 1, 'sind == len(line_exc) - 1    -     точно нет совпадений между ключом и исклом (искл простое слово без звёзд)', line_key, line_exc)
                #     break

    # ключ - абв* - ключ
    if word_from_line_key[0] != '*' and word_from_line_key[len(word_from_line_key) - 1] == '*':
        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - *а*бв* или *абв*
            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) == len(
                    word_from_line_key[:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[1:len(word_from_line_exc) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da8')
                        break
            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) > len(
                    word_from_line_key[:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                        #print(letter_key, letter_exc, word_from_line_key[:len(word_from_line_key) - 1], word_from_line_exc[1:len(word_from_line_exc) - 1])

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key[:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da9', word_from_line_key, word_from_line_exc)
                        break
        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*':  # искл - *абв или *а*бв
            if len(word_from_line_exc[1:]) == len(word_from_line_key[:len(word_from_line_key) - 1]) and (
                    word_from_line_key[len(word_from_line_key) - 2] == word_from_line_exc[len(word_from_line_exc) - 1] or word_from_line_key[len(word_from_line_key) - 2] == '.' or word_from_line_exc[
                len(word_from_line_exc) - 1] == '.'):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[1:]):
                        fix_match_word_key_and_exc = 1
                        #print('da10')
                        break
            if len(word_from_line_exc[1:]) > len(word_from_line_key[:len(word_from_line_key) - 1]) and (word_from_line_key[0] == word_from_line_exc[1] or word_from_line_key[0] == '.' or word_from_line_exc[
                1] == '.'):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key[:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da11')
                        break
        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - абв* или а*бв*
            if len(word_from_line_exc[:len(word_from_line_exc) - 1]) == len(word_from_line_key[:len(word_from_line_key) - 1]) and (word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[0] == '.'):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_key) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[:len(word_from_line_exc) - 1]) - 1:
                        fix_match_word_key_and_exc = 1
                        #print('da12')
                        break
            if len(word_from_line_exc[:len(word_from_line_exc) - 1]) > len(word_from_line_key[:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_key) - 1]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key[:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da13')
                        break
        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc):  # искл аб*в
            if len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]) == len(word_from_line_key[:len(word_from_line_key) - 1]) and (
                    word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[
                0] == '.'):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                ##print(line_key, line_exc)
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]):
                        fix_match_word_key_and_exc = 1
                        #print('da14')
                        break
            if len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]) > len(
                    word_from_line_key[:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:len(word_from_line_key) - 1]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]))):  # проверка межзвёзднной части на совпадение
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key[:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da15')
                        break
        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc) == None and (
                word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[0] == '.'):  # искл - слово без звёзд. обычное слово
            ##print(word_from_line_key, word_from_line_key, 'ворсловоключискл')
            counter_match = 0
            fix_index_letter_key = 0
            fix_index_letter_exc = 0
            for index_letter_key, letter_key in list(enumerate(word_from_line_key[:len(word_from_line_key) - 1])):
                for index_letter_exc, letter_exc in list(enumerate(word_from_line_exc)):  # проверка межзвёзднной части на совпадение
                    if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc + 1 and index_letter_key == fix_index_letter_key + 1):
                        ##print(letter_key , letter_exc, word_from_line_key, word_from_line_exc)
                        ##print('prohodit dalshe', letter_key , index_letter_key, letter_exc, index_letter_exc, word_from_line_key[:len(word_from_line_key) - 1 ], word_from_line_exc)
                        if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                            ##print(letter_key, letter_exc)
                            fix_index_letter_key = index_letter_key
                            fix_index_letter_exc = index_letter_exc
                            counter_match += 1
                            break
                        else:
                            fix_index_letter_key = index_letter_key
                            fix_index_letter_exc = index_letter_exc
                if counter_match == len(word_from_line_key[:len(word_from_line_key) - 1]):
                    fix_match_word_key_and_exc = 1
                    #print('da16')
                    break

    # ключ - *абв - ключ
    if word_from_line_key[0] == '*' and word_from_line_key[len(word_from_line_key) - 1] != '*':
        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - *а*бв* или *абв*
            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) == len(
                    word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[1:len(word_from_line_exc) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da17')
                        break
            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) > len(
                    word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key[1:len(word_from_line_key)]):
                        fix_match_word_key_and_exc = 1
                        #print('da18')
                        break
        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*':  # искл - *абв или *а*бв
            if len(word_from_line_exc[1:]) == len(word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1) and word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1]:
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[1:]):
                        fix_match_word_key_and_exc = 1
                        #print('da19')
                        break
            if len(word_from_line_exc[1:]) > len(word_from_line_key[1:len(word_from_line_key) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1) and word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1]:
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key[1:len(word_from_line_key)]):
                        fix_match_word_key_and_exc = 1
                        #print('da20')
                        break
        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - абв* или а*бв*
            if len(word_from_line_exc[:len(word_from_line_exc) - 1]) == len(word_from_line_key[1:]) and (word_from_line_key[1] == word_from_line_exc[0] or word_from_line_key[1] == '.' or word_from_line_exc[0] == '.'):

                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                                ##print(num, '   ', len(line_exc[:len(line_exc) - 1]))
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[:len(word_from_line_exc) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da21_000')
                        break

            if len(word_from_line_exc[1:]) > len(word_from_line_key[:len(word_from_line_key) - 1]) and (
                    word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 2] or word_from_line_key[len(word_from_line_key) - 1] == '.' or word_from_line_exc[len(word_from_line_exc) - 2] == '.'):
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[:len(word_from_line_key) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da21_111')
                        break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc):  # искл аб*в
            if len(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]) == len(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]) and (
                    word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1] or word_from_line_key[len(word_from_line_key) - 1] == '.' or word_from_line_exc[
                len(word_from_line_exc) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):

                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]):
                        fix_match_word_key_and_exc = 1
                        #print('da23')
                        break
            if len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]) > len(word_from_line_key[1:len(word_from_line_key) - 1]) and (
                    word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1] or word_from_line_key[len(word_from_line_key) - 1] == '.' or word_from_line_exc[
                len(word_from_line_exc) - 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]))):  # проверка межзвёзднной части на совпадение
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                                ##print(num)
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key[(re.search('\*', word_from_line_exc)).start():]):
                        fix_match_word_key_and_exc = 1
                        #print('da24')
                        break
        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc) == None and (
                word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1] or word_from_line_key[len(word_from_line_key) - 1] == '.' or word_from_line_exc[len(word_from_line_exc) - 1] == '.'):  # искл - слово без звёзд. обычное слово
            counter_match = 0
            fix_index_letter_key = 0
            fix_index_letter_exc = 0
            ##print('1258', word_from_line_key[1:], word_from_line_exc)
            for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[1:]))):
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc))):  # проверка межзвёзднной части на совпадение

                    if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                        if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                            fix_index_letter_key = index_letter_key
                            fix_index_letter_exc = index_letter_exc
                            counter_match += 1
                        else:
                            fix_index_letter_key = index_letter_key
                            fix_index_letter_exc = index_letter_exc
                if counter_match == len(word_from_line_key[1:len(word_from_line_key)]):
                    fix_match_word_key_and_exc = 1
                    #print('da25', word_from_line_key, word_from_line_exc)
                    break

    # ключ - а*бв - ключ
    if word_from_line_key[0] != '*' and word_from_line_key[len(word_from_line_key) - 1] != '*' and re.search('\w+\*\w+', word_from_line_key):


        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*':  # искл - *абв или *а*бв
            if len(word_from_line_exc[1:]) == len(
                    word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1) and word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1]:
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[1:]):
                        fix_match_word_key_and_exc = 1
                        #print('da19')
                        break
            if len(word_from_line_exc[1:]) > len(
                    word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1) and word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1]:
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]):
                        fix_match_word_key_and_exc = 1
                        #print('da20')
                        break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - абв* или а*бв*
            if len(word_from_line_exc[:len(word_from_line_exc) - 1]) == len(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]) and (
                    word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[0] == '.'):
                counter_match = 0

                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                ##print(num, '   ', len(line_exc[:len(line_exc) - 1]))
                    if counter_match == len(word_from_line_exc[:len(word_from_line_exc) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da31')
                        break

            if len(word_from_line_exc[1:]) > len(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]) and (
                    word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 2] or word_from_line_key[len(word_from_line_key) - 1] == '.' or word_from_line_exc[len(word_from_line_exc) - 2] == '.'):
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                ##print(len(line_key[:(re.search('\*', line_key)).start()]))
                    if counter_match == len(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]):
                        fix_match_word_key_and_exc = 1
                        #print('da32')
                        break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc) and (
                word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[0] == '.') and (
                word_from_line_key[len(word_from_line_key) - 1] == word_from_line_exc[len(word_from_line_exc) - 1] or word_from_line_key[len(word_from_line_key) - 1] == '.' or word_from_line_exc[
            len(word_from_line_exc) - 1] == '.'):  # искл аб*в
            if len(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]) == len(
                    word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):

                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]):
                        if len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start() + 1]) == len(
                                word_from_line_key[:(re.search('\*', word_from_line_key)).start() + 1]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд

                            counter_match = 0
                            fix_index_letter_key = 0
                            fix_index_letter_exc = 0
                            for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]))):  # проверка межзвёзднной части на совпадение
                                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]))):
                                    if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                                        if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                            fix_index_letter_key = index_letter_key
                                            fix_index_letter_exc = index_letter_exc
                                            counter_match += 1
                                        else:
                                            fix_index_letter_key = index_letter_key
                                            fix_index_letter_exc = index_letter_exc
                                ##print(line_key, line_exc, num, len(line_exc[:(re.search('\*', line_exc)).start()]))
                                if counter_match == len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]):
                                    fix_match_word_key_and_exc = 1
                                    #print('da331')
                                    break

                        if len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]) > len(
                                word_from_line_key[:(re.search('\*', word_from_line_key)).start()]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                            counter_match = 0
                            fix_index_letter_key = 0
                            fix_index_letter_exc = 0
                            for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]))):
                                for index_letter_exc, letter_exc in reversed(
                                        list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]))):  # проверка межзвёзднной части на совпадение
                                    if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                                        if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                            fix_index_letter_key = index_letter_key
                                            fix_index_letter_exc = index_letter_exc
                                            counter_match += 1
                                        else:
                                            fix_index_letter_key = index_letter_key
                                            fix_index_letter_exc = index_letter_exc
                                if counter_match == len(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]):
                                    fix_match_word_key_and_exc = 1
                                    #print('da332')
                                    break

            if len(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]) > len(
                    word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]))):  # проверка межзвёзднной части на совпадение
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]):

                        if len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]) == len(
                                word_from_line_key[:(re.search('\*', word_from_line_key)).start()]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                            counter_match = 0
                            fix_index_letter_key = 0
                            fix_index_letter_exc = 0
                            for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]))):  # проверка межзвёзднной части на совпадение
                                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]))):
                                    if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                                        if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                            fix_index_letter_key = index_letter_key
                                            fix_index_letter_exc = index_letter_exc
                                            counter_match += 1
                                        else:
                                            fix_index_letter_key = index_letter_key
                                            fix_index_letter_exc = index_letter_exc
                                if counter_match == len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]):
                                    fix_match_word_key_and_exc = 1
                                    #print('da341')
                                    break

                        if len(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]) > len(
                                word_from_line_key[:(re.search('\*', word_from_line_key)).start()]):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                            counter_match = 0
                            fix_index_letter_key = 0
                            fix_index_letter_exc = 0
                            for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]))):
                                for index_letter_exc, letter_exc in reversed(
                                        list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()]))):  # проверка межзвёзднной части на совпадение
                                    if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                                        if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                            fix_index_letter_key = index_letter_key
                                            fix_index_letter_exc = index_letter_exc
                                            counter_match += 1
                                        else:
                                            fix_index_letter_key = index_letter_key
                                            fix_index_letter_exc = index_letter_exc
                                if counter_match == len(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]):
                                    fix_match_word_key_and_exc = 1
                                    #print('da342')
                                    break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc) == None and (
                word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[0] == '.') and (
                word_from_line_exc[len(word_from_line_exc) - 1] == word_from_line_key[len(word_from_line_key) - 1] or word_from_line_exc[len(word_from_line_exc) - 1] == '.' or word_from_line_key[
            len(word_from_line_key) - 1] == '.'):  # искл - слово без звёзд. обычное слово
            line_key_izm = word_from_line_key[:(re.search('\*', word_from_line_key)).start()] + word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]
            if len(line_key_izm) == len(word_from_line_exc):
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(line_key_izm))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc):
                        fix_match_word_key_and_exc = 1
                        #print('da35')
                        break
            if len(line_key_izm) < len(word_from_line_exc):
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in list(enumerate(word_from_line_key[:(re.search('\*', word_from_line_key)).start()])):  # проверка межзвёзднной части на совпадение
                    for index_letter_exc, letter_exc in list(enumerate(word_from_line_exc)):
                        if ((fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc - 1 == fix_index_letter_exc and index_letter_key - 1 == fix_index_letter_key)) and index_letter_key == index_letter_exc:
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                ##print('shodka')
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                                break
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key[:(re.search('\*', word_from_line_key)).start()]):
                        counter_match = 0
                        fix_index_letter_key = 0
                        fix_index_letter_exc = 0
                        for index_letter_key, letter_key in reversed(
                                list(enumerate(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]))):  # проверка межзвёзднной части на совпадение
                            for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc))):
                                if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                                    if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                        fix_index_letter_key = index_letter_key
                                        fix_index_letter_exc = index_letter_exc
                                        counter_match += 1
                                    else:
                                        fix_index_letter_key = index_letter_key
                                        fix_index_letter_exc = index_letter_exc
                            if counter_match == len(word_from_line_key[(re.search('\*', word_from_line_key)).start() + 1:]):
                                fix_match_word_key_and_exc = 1
                                #print('da36')
                                break

    # ключ - абв - ключ
    if word_from_line_key[0] != '*' and word_from_line_key[len(word_from_line_key) - 1] != '*' and re.search('\w+\*\w+', word_from_line_key) == None:
        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*':  # искл - *абв*
            ##print('бобонька')
            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) == len(word_from_line_key):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0

                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[1:len(word_from_line_exc) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da411')
                        break
            if len(word_from_line_exc[1:len(word_from_line_exc) - 1]) > len(word_from_line_key):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                ##print(index_letter_key, letter_key,'--', index_letter_exc, letter_exc,'--', word_from_line_key, word_from_line_exc)
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[1:len(word_from_line_exc) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da412', word_from_line_key, word_from_line_exc)
                        break

        if word_from_line_exc[0] == '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and (
                word_from_line_exc[len(word_from_line_exc) - 1] == word_from_line_key[len(word_from_line_key) - 1] or word_from_line_exc[len(word_from_line_exc) - 1] == '.' or word_from_line_key[
            len(word_from_line_key) - 1] == '.'):  # искл - *абв
            if len(word_from_line_exc[1:]) == len(word_from_line_key):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[1:]):
                        fix_match_word_key_and_exc = 1
                        #print('da421')
                        break
            if len(word_from_line_exc[1:]) > len(word_from_line_key):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[1:]))):  # проверка межзвёзднной части на совпадение

                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key):
                        fix_match_word_key_and_exc = 1
                        #print('da422')
                        break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] == '*' and (word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[0] == '.'):  # искл - абв*
            if len(word_from_line_exc[:len(word_from_line_exc) - 1]) == len(word_from_line_key):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_exc[:len(word_from_line_exc) - 1]):
                        fix_match_word_key_and_exc = 1
                        #print('da431')
                        break
            if len(word_from_line_exc[:len(word_from_line_exc) - 1]) > len(word_from_line_key):  # сравнить к и и  - начать итерацию, в зависимости от размера меж звёзд
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):
                    for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[:len(word_from_line_exc) - 1]))):  # проверка межзвёзднной части на совпадение
                        ##print(letter_key, letter_exc)
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                ##print(counter_match, counter_match)
                    ##print(counter_match , len(word_from_line_key), 'проверить da432')
                    if counter_match == len(word_from_line_key):
                        fix_match_word_key_and_exc = 1
                        #print('da432')
                        break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc) and (
                word_from_line_key[0] == word_from_line_exc[0] or word_from_line_key[0] == '.' or word_from_line_exc[0] == '.') and (
                word_from_line_exc[len(word_from_line_exc) - 1] == word_from_line_key[len(word_from_line_key) - 1] or word_from_line_exc[len(word_from_line_exc) - 1] == '.' or word_from_line_key[
            len(word_from_line_key) - 1] == '.'):  # искл - слово без звёзд. обычное слово
            line_exc_izm = word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()] + word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]
            if len(line_exc_izm) == len(word_from_line_key):
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):  # проверка межзвёзднной части на совпадение
                    for index_letter_exc, letter_exc in reversed(list(enumerate(line_exc_izm))):
                        if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key):
                        fix_match_word_key_and_exc = 1
                        #print('da46')
                        break
            if len(line_exc_izm) < len(word_from_line_key):
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_exc, letter_exc in list(enumerate(word_from_line_exc[:(re.search('\*', word_from_line_exc)).start()])):  # проверка межзвёзднной части на совпадение
                    for index_letter_key, letter_key in list(enumerate(word_from_line_key)):
                        if ((fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc - 1 == fix_index_letter_exc and index_letter_key - 1 == fix_index_letter_key)) and index_letter_key == index_letter_exc:
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                ##print('shodka22')
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                                break
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc


                    if counter_match == len(word_from_line_key[:(re.search('\*', word_from_line_exc)).start()]):
                        counter_match = 0
                        fix_index_letter_key = 0
                        fix_index_letter_exc = 0
                        for index_letter_exc, letter_exc in reversed(list(enumerate(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]))):  # проверка межзвёзднной части на совпадение
                            for index_letter_key, letter_key in reversed(list(enumerate(word_from_line_key))):
                                if (fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc == fix_index_letter_exc - 1 and index_letter_key == fix_index_letter_key - 1):
                                    if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                        fix_index_letter_key = index_letter_key
                                        fix_index_letter_exc = index_letter_exc
                                        counter_match += 1
                                    else:
                                        fix_index_letter_key = index_letter_key
                                        fix_index_letter_exc = index_letter_exc
                            if counter_match == len(word_from_line_exc[(re.search('\*', word_from_line_exc)).start() + 1:]):
                                fix_match_word_key_and_exc = 1
                                #print('da47')
                                break

        if word_from_line_exc[0] != '*' and word_from_line_exc[len(word_from_line_exc) - 1] != '*' and re.search('\w+\*\w+', word_from_line_exc) == None and re.fullmatch('\d+\®\d+', word_from_line_exc) == None:  # искл - слово без звёзд. обычное слово
            if len(word_from_line_key) == len(word_from_line_exc):
                counter_match = 0
                fix_index_letter_key = 0
                fix_index_letter_exc = 0
                for index_letter_key, letter_key in list(enumerate(word_from_line_key)):  # проверка межзвёзднной части на совпадение
                    for index_letter_exc, letter_exc in list(enumerate(word_from_line_exc)):
                        if ((fix_index_letter_key == 0 and fix_index_letter_exc == 0) or (index_letter_exc - 1 == fix_index_letter_exc and index_letter_key - 1 == fix_index_letter_key)) and index_letter_key == index_letter_exc:
                            if letter_key == letter_exc  or letter_key == '.' or (letter_key == '£' and re.fullmatch('\d', letter_exc)) or (letter_exc == '£' and re.fullmatch('\d', letter_key)):
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                                counter_match += 1
                                break
                            else:
                                fix_index_letter_key = index_letter_key
                                fix_index_letter_exc = index_letter_exc
                    if counter_match == len(word_from_line_key):
                        fix_match_word_key_and_exc = 1
                        #print('da50')
                        break

    # ключ-искл - .* - ключ-искл
    if word_from_line_exc == '.*' or word_from_line_key == '.*':
        fix_match_word_key_and_exc = 1
        #print('da51')

    return fix_match_word_key_and_exc
def compare_lines_new(str1, str2):
    num_word1 = 0
    match = 0
    nl1 = []
    for index1, slovo1 in enumerate(str1.split()):
        if re.fullmatch('\d+\®\d+', slovo1) == None:
            num_word1 += 1
            nl1.append(slovo1)
        if re.fullmatch('\d+\®\d+', slovo1):
            #print('проверить-', int(slovo1.split('®')[1]))
            for raz in range(int(slovo1.split('®')[1])):
                nl1.append('®')
    nl2 = []
    for index2, slovo2 in enumerate(str2.split()):
        if re.fullmatch('\d+\®\d+', slovo2) == None:
            num_word1 += 1
            nl2.append(slovo2)
        if re.fullmatch('\d+\®\d+', slovo2):
            for raz in range(int(slovo2.split('®')[1])):
                nl2.append('®')
    str1 = nl1
    str2 = nl2
    #print(str1, '\n', str2)


    rezervstr1 = str1
    rezervstr2=str2
    flag_rezult = 0
    marker=0
    while flag_rezult==0 and str2!=[] :
        #print('новое значение строки str2--', type(str2), str2)
        fix1=0
        fix2=0
        sp_indexs1=[]
        sp_indexs2=[]
        signal=0
        marker+=1
        factor=0
        notrast1=0
        notrast2 = 0
        for index_item,item in enumerate(str1):
            if signal==1:
                break
            for index_ktem, ktem in enumerate(str2):
                #print('до признания1--', item, ktem, '--',  index_item, fix1, '--',factor, '--',index_ktem,fix2, '--', str1, str2)
                if (compare_words(item, ktem)==1 or item=='®' or ktem=='®') and ((fix1 == 0 and fix2 == 0 and factor==0 ) or (index_item == fix1 + 1 and index_ktem == fix2 + 1)):
                    if '®' not in item:
                        notrast1 = 1
                    if '®' not in ktem:
                        notrast2 = 1
                    if index_item not in sp_indexs1:
                        sp_indexs1.append(index_item)
                        #print('добавление в список1-', sp_indexs1, item, ktem)
                    if len(str2)-1-index_ktem not in sp_indexs2:
                        sp_indexs2.append(len(str2) - 1 - index_ktem)
                        #print('добавление в список2-', sp_indexs2, item, ktem)
                    if index_ktem == len(str2) - 1:
                        #print('случился брик1', index_ktem, len(str2) - 1, str1)
                        signal = 1
                        break
                    fix1=index_item
                    fix2=index_ktem
                    factor=1
                    #print('после призанния1--', item, ktem, '--',  index_item, fix1, '--',index_ktem,fix2, '--', str1, str2)
                    break

        if (len(sp_indexs1) == len(str1) or len(sp_indexs2) == len(str2)) and notrast1 == 1 and notrast2 == 1 and marker<=1 :
            #print('missing complete00', sp_indexs1, str1, '--',sp_indexs2,  str2, '--',len(sp_indexs1) , len(str1) , len(sp_indexs2) , len(str2),sp_indexs2,str2, str1[sp_indexs1[0]:sp_indexs1[len(sp_indexs1)-1]+1], str2[sp_indexs2[0]:sp_indexs2[len(sp_indexs2)-1]+1])
            flag_rezult = 1
            return flag_rezult
        sp_indexs2=list(reversed(sp_indexs2))
        #print(sp_indexs1, sp_indexs2)
        per3=[item for index_item,item in enumerate(sp_indexs1) if item in sp_indexs2]
        if per3==[]:
            flag_rezult = 0
            str2=str2[1:]
            #print('пустой список1')

        #print(per3)
        count=0
        for index_i, i in enumerate(per3):

            if index_i==i and str1[per3[len(per3)-1]]!='®': #добавилось обновление
                #print('тандыр-',index_i, i)
                count+=1
                if count==len(per3):
                    #print('missing complete')
                    flag_rezult=1
                    return flag_rezult
            if index_i==len(per3)-1 and count!=len(per3):
                #print('missing failed')
                flag_rezult = 0
                str2 = str2[1:]


    if flag_rezult == 0:
        str2 = rezervstr2
        str1 = rezervstr1
        #print('до вступления в резерв-', str1)
        while flag_rezult == 0 and str1 != []:
            #print('заступаем на новое========================================================')
            #print('новое значение строки str1--', type(str1), str1)
            fix1=0
            fix2=0
            sp_indexs1=[]
            sp_indexs2=[]
            signal=0
            #print('резервный--',str2, str1)

            factor=0
            for index_item,item in enumerate(str2):
                if signal==1:
                    break
                for index_ktem, ktem in enumerate(str1):
                    #print('до признания2--', item, ktem, '--',  index_item, fix1, '--',fix2,index_ktem, '--', str2, str1)
                    if (compare_words(item, ktem)==1 or item=='®' or ktem=='®') and ((fix1 == 0 and fix2 == 0 and factor==0)  or (index_item == fix1 + 1 and index_ktem == fix2 + 1)):
                        if index_item not in sp_indexs1:
                            sp_indexs1.append(index_item)
                        if len(str1)-1-index_ktem not in sp_indexs2:
                            sp_indexs2.append(len(str1) - 1 - index_ktem)
                        if index_ktem == len(str1) - 1:
                            #print('случился брик2', index_ktem , len(str1) - 1, str1)
                            signal = 1
                            break
                        fix1=index_item
                        fix2=index_ktem
                        factor=1
                        break
            sp_indexs2=list(reversed(sp_indexs2))
            #print(sp_indexs1, sp_indexs2)
            per3=[item for index_item,item in enumerate(sp_indexs1) if item in sp_indexs2]
            if per3==[]:
                flag_rezult = 0
                str1= str1[1:]
                #print('пустой список2')

            #print(per3)
            count=0
            for index_i, i in enumerate(per3):
                #print(index_i, '--',i, 'внутри')
                if index_i==i and str2[per3[len(per3)-1]]!='®': #добавилось обновление:
                    #print('индекс i - цифра               ',index_i, i)
                    count+=1
                    if count==len(per3):
                        #print('missing complete2')
                        flag_rezult=1
                        return flag_rezult
                if index_i==len(per3)-1 and count!=len(per3):
                    #print('missing failed2')
                    str1 = str1[1:]
                    flag_rezult = 0
    if flag_rezult == 0:
        return flag_rezult
def add_dist(a):
    while re.search(' \d*\®\d* ', a):
        z_start = int(re.search(' \d*\®\d* ', a).start() )
        z_end = int(re.search(' \d*\®\d* ', a).end())-1
        a=a[:z_start]+'¢'+a[z_start+1:z_end]+'¢'+a[z_end+1:]
    a=a.replace(' ',' 0®0 ').replace('¢',' ')
    return a
def timeit(func):
    def wrapper(orig_index_line1, dict1, dictplus, dictminus):
        global total_time
        t_start = time.monotonic()
        func(orig_index_line1, dict1, dictplus, dictminus)
        t_stop = time.monotonic()
        t_run = t_stop - t_start
        one_time = round(t_run, 1)
        total_time = total_time + one_time
        left_time = time.strftime("%H:%M:%S", time.gmtime((len(original_list) - counter_line_from_orig_list_key) * round(total_time / counter_line_from_orig_list_key, 1)))
        try:
            print(f'{round(counter_line_from_orig_list_key+1, 1)} пройдено из {len(original_list)}   |   ',    time.strftime("%H:%M:%S", time.gmtime(round(total_time, 1))), 'прошло со старта   |   ', round(one_time, 1), 'сек. время этой операции   |   ', round(total_time / counter_line_from_orig_list_key, 1) , 'cреднее время одной строки сек   |   ',  left_time, "осталось до конца программы   |   ",  len(dict1[orig_index_line1+1]), "строк в след строке   |   ",  original_list[orig_index_line1+1][:30], f" --- след строка {round(counter_line_from_orig_list_key+2, 1)}   |   ", datetime.datetime.now().strftime('%H:%M:%S'))
        except IndexError:
            pass
        #print(orig_line1)

    return wrapper
#@timeit
#def main_compare(orig_index_line1, dict1, dictplus, dictminus):
def get_all_elements_in_list_of_lists(list):
    count_elem = 0
    for element in list:
        count_elem += len(element)
    return count_elem
def show_big_lines(list):
    dict_big_line = []
    for indexel, element in enumerate(list):
        if len(element)>10:
            dict_big_line.append(original_list[indexel])
    return dict_big_line
def perebor(i):
    i=str(i)
    i=i[1:len(i)-1]
    i=i.replace('"', '').replace("'", "")
    #print(i)
    return i


original_list1=file('C:\\tmp\\rezult_compare_keys_exc.txt')
original_list2=file('C:\\tmp\\exc_sui.txt')

num_reg=0
dict1=[]
for original_line1 in original_list1:
    a1=Counter(original_line1)['|']
    if a1==0:
        a1=1
    elif a1==1:
        a1=2
    b1=Counter(original_line1)['[']
    if b1==0:
        b1=1
    elif b1==1:
        b1=2
    c1=Counter(original_line1)['?']
    if c1==0:
        c1=1
    elif c1==1:
        c1=2
    if a1*b1*c1 <120:
        #print(num_reg, ' из 1го ', len(original_list1), '--', a1,b1,c1, ' ---',a1*b1*c1, '--', original_line1)
        dict1.append(repreg(original_line1))
        num_reg += 1
    else:
        dict1.append([original_line1])
num_reg=0
dict2=[]
for original_line2 in original_list2:
    #print(original_line2)
    a1=Counter(original_line2)['|']
    if a1==0:
        a1=1
    elif a1==1:
        a1=2
    b1=Counter(original_line2)['[']
    if b1==0:
        b1=1
    elif b1==1:
        b1=2
    c1=Counter(original_line2)['?']
    if c1==0:
        c1=1
    elif c1==1:
        c1=2
    if a1*b1*c1 <80:
        #print(num_reg, ' из 2го', len(original_list2), a1, b1, c1, ' ---', a1 * b1 * c1, '--', original_line2)
        dict2.append(repreg(original_line2))
        num_reg += 1
    else:
        dict2.append([original_line2])
dict3= []
dictforrecordfile=[]
def comparing(dict1, dict2):
    total_time = 0
    counter_line_from_orig_list_key = 0
    count_orig_line1 = 0
    for orig_index_line1, orig_line1 in enumerate(dict1):
        print(orig_index_line1, '-только из первого словаря-', len(dict1), '--',original_list1[orig_index_line1])
        count_orig_line1 += 1
        counter_line_from_orig_list_key += 1
        count_orig_line2 = 0
        for orig_index_line2, orig_line2 in enumerate(dict2):
            count_orig_line2 += 1
            print(orig_index_line1, 'из первого словаря', len(dict1), '---'  ,count_orig_line2, 'из второго словаря ',  len(dict2) , original_list1[orig_index_line1], '---', original_list2[orig_index_line2])
            count_match = 0
            signal_stop = 0
            for new_line1 in dict1[orig_index_line1]:
                if signal_stop == 1:
                    break
                for new_line2 in dict2[orig_index_line2]:
                    if compare_lines_new(new_line1, new_line2) == 1 and ('*' not in new_line2[0] or '*' not in new_line2[len(new_line2)-1]) and ' .* ' not in new_line2:
                        count_match += 1
                        dictforrecordfile.append(str(original_list1[orig_index_line1])+ '<-->'+ str(original_list2[orig_index_line2])+ '<-->'+  str(new_line1)+ '<-->'+  str(new_line2))
                        #print(original_list1[orig_index_line1], '<-->', original_list2[orig_index_line2], '------------------', new_line1, '---', new_line2)
                        #print('<-->',new_line1, '---', new_line2)
                        dict3.append(original_list1[orig_index_line1])
                        signal_stop = 1
                        break
list(map(comparing, [dict1], [dict2]))
print( 'третий словарь - в виде списка--',  dict3)
dict4=[]
for original_line1 in original_list1:
    if original_line1 not in set(dict3):
        dict4.append(original_line1+', 0')
dict3=list(dict(Counter(dict3)).items())
dict3=list(map(perebor, dict3)    )
dict3=dict3+dict4
print( 'третий словарь после соединения- в конце --',  dict3)
file_for_record3 = open(f'C:\\tmp\\rezult_count_keys.txt', 'w')
for newlinerec in dict3:
    newlinerec=str(newlinerec)
    file_for_record3.write(str(newlinerec + '\n'))
file_for_record3.close()

file_for_record4 = open(f'C:\\tmp\\logi_count_keys.txt', 'w', encoding="utf-8")
for newlinerec in dictforrecordfile:
    newlinerec=str(newlinerec)
    file_for_record4.write(str(newlinerec + '\n'))
file_for_record4.close()







