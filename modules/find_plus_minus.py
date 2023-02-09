# программа обращается к бд и выводит в csv список материалов по тегу, выбирая статус темы
import pandas as pd
import psycopg2
from psycopg2 import Error

def find_regs(status, type_text):
    # SOURCES_SETTINGS = {
    #     'user': '***',
    #     'password': '***',
    #     'host': '192.168.70.120',
    #     'port': '5432',
    #     'dbname': 'an_tags'
    # }
    # try:
    #     # Подключение к существующей базе данных
    #     connection = psycopg2.connect(**SOURCES_SETTINGS)
    #     cursor = connection.cursor()
    #     print("Соединение началось")
    #     # Курсор для выполнения операций с базой данных
    #     cursor.execute(f"""
    # SELECT created_at, url, text, status, all_tags FROM public."sim_materialcard"
    # where status='{status}' and violation='{type_text}'
    # order by created_at desc
    #     """)
    #     # status='2' - принятые материалы
    #     # status='3' - отклонённые материалы
    #     # type_text - номер темы
    #
    #     count_mix = cursor.fetchall()
    # except (Exception, Error) as error:
    #     print("Ошибка при работе с PostgreSQL", error)
    # finally:
    #     if connection:
    #         cursor.close()
    #         connection.close()
    #         print("Соединение с PostgreSQL закрыто")
    # spisok_reg = pd.DataFrame(count_mix)
    if status ==2:
        spisok_reg = pd.read_csv('docs/sim_sui_prinyato.csv')
        spisok_reg.columns = ["Дата", "Ссылка", "Текст", "Статус", "all_tags"]
        spisok_reg.to_csv(f'docs/spisok_reg_{status}.csv')
        return spisok_reg
    if status == 3:
        spisok_reg = pd.read_csv('docs/sim_sui_otkl.csv')
        spisok_reg.columns = ["Дата", "Ссылка", "Текст", "Статус", "all_tags"]
        spisok_reg.to_csv(f'docs/spisok_reg_{status}.csv')
        return spisok_reg

