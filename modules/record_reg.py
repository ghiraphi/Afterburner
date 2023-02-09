#запись в бд обновлённых словарей
# def rec_reg_db(new_list_reg, name_type, num_dict):
#     import psycopg2
#     from psycopg2 import Error
#     SOURCES_SETTINGS = {
#         'user': '***',
#         'password': '***',
#         'host': '192.168.70.120',
#         'port': '5432',
#         'dbname': 'an_tags'
#     }
#     try:
#         # Подключение к существующей базе данных
#         connection = psycopg2.connect(**SOURCES_SETTINGS)
#         cursor = connection.cursor()
#         print("Соединение началось")
#         # Курсор для выполнения операций с базой данных
#         cursor.execute(f"""
#     UPDATE public.dictionary SET raw_regexps = {new_list_reg} WHERE type='{name_type}' and dict={num_dict}
#         """)
#     # type - 'keys' или 'exclusion'
#     # handbook_id - номер словаря
#     # raw_regexps - список регулярок из конкретного словаря
#
#         count_mix = cursor.fetchall()
#     except (Exception, Error) as error:
#         print("Ошибка при работе с PostgreSQL", error)
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()
#             print("Соединение с PostgreSQL закрыто")

import psycopg2
from psycopg2 import Error
def rec_reg_db(new_list_reg, name_type, num_dict):
    name_file=f'docs/new_{name_type}_{num_dict}.txt'
    with open(name_file, "w", encoding="utf-8") as file:
        for newlinerec in new_list_reg:
            #print(newlinerec, type(newlinerec))
            file.write(newlinerec + '\n')
        file.close()
