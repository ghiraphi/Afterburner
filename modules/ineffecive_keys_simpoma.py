# программа удаляет ключи, которые не показывали эфективность,
# используя отношение принятых и отклонённых из симпомы соединяет с исходным списком ключей
# сохраняет новый список ключей в csv
import re
import pandas as pd
import modules.get_reg_db
import modules.accuracy_violance
import modules.choose_dict

def del_keys(tabl_prin,tabl_otkl):
    #подключение к таблице идёт через базу данных сервера компании,
    # но в тестовом варианте предлагается вариант с использованием локального csv
    numb_viol = modules.choose_dict.filtr_dict_numb(modules.accuracy_violance.list_dicts)  # выбран номер темы для работы
    # with open("C:\\tmp\sui_keys_before.txt") as file:
    #     spisok=[item.rstrip() for item in file]
    spisok=[item.rstrip() for item in modules.get_reg_db.get_list_reg('keys', numb_viol)]
    print(len(spisok), spisok, '-количество ключей исходных')
    # объединение принятых и отклонённых ключей
    df3 = tabl_prin.merge(tabl_otkl, left_on=0, right_on=0, how='outer')
    df3['otnosh']=df3['stat_koef_x']-df3['stat_koef_y'] #разница долей между принятыми и отклонёнными
    df3=df3.sort_values(by='otnosh',ascending=False)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', 20)
    t_sfor = df3[(df3['1_x'] < 20)  | (df3['otnosh'] < (-0.46))] # фильтрация ключей, где
    # df3['1_x'] - отработало более 20 в принятых,
    # df3['otnosh'] - разница долей, где количество принятых регулярок относительных величинах больше чем отклонённых

    spisok_klychey=t_sfor[0].tolist()
    spisok_klychey2=[i.replace('?:','').replace('$;(',' ').replace(');^',' ').replace(')(\\W+\\w+){',' ').replace('}\\W+(',' ').replace('0, ', '0,').replace('$;0', '').replace('[^\\W]', '').replace('\\S?', '.?').replace('\\S*', '*').replace('\\S', '.').replace('\\b', '').replace('.*', '*').replace(';(', ' ').replace('^', '').replace('$;', '').replace('; ', ' ').replace('()', '(.)').replace('}\\W*(', ' ').replace(';0', '').replace(');', ' ').replace(';, ', ' ') for i in spisok_klychey]
    spisok_klychey2=[i[1:len(i)-1] if (re.search('^\(\(\(', i) and re.search('\)$', i) or (re.search('^\(', i) and re.search('\)\)\)$', i))) else i for i in spisok_klychey2 ]
    spisok_klychey2=[i[1:len(i)-1] if ((re.search('^\([^\(]', i) and re.search('\)$', i)) or (re.search('^\(', i) and re.search('^[^\)]\)$', i))) else i for i in spisok_klychey2 ]
    # spisok_klychey2=[i.replace('|(видео*)|', '|') if re.search('.*видео.*', i) else i for i in spisok_klychey2]
    print(len(spisok_klychey2), '-количество ключей, которые не прошли фильтрацию')

    result=list(set(spisok) - set(spisok_klychey2)) # все текущие ключи минус ключи, которые не вошли в фильтр
    print(len(result), result, 'ключи, которые нужно оставить. формула = все текущие ключи минус ключи, которые не вошли в фильтр')


    file_for_record = open(f'docs/new_keys.txt', 'w', encoding="utf-8")
    for newlinerec in result:
        newlinerec=str(newlinerec)
        file_for_record.write(str(newlinerec + '\n'))
    file_for_record.close()
    return result #возвращает список новых ключей после сокращения