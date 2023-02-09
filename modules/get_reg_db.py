# подсчёт количества ключей и исключений в одном словаре
import psycopg2
from psycopg2 import Error


def get_list_reg(name_type, num_dict):



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
    # SELECT type, handbook_id, raw_regexps FROM public.dictionary
    # where
    # type='{name_type}' and handbook_id={num_dict}
    #     """)
    # # type - 'keys' или 'exclusion'
    # # handbook_id - номер словаря
    # # raw_regexps - список регулярок из конкретного словаря
    #
    #     count_mix = cursor.fetchall()
    # except (Exception, Error) as error:
    #     print("Ошибка при работе с PostgreSQL", error)
    # finally:
    #     if connection:
    #         cursor.close()
    #         connection.close()
    #         print("Соединение с PostgreSQL закрыто")
    #
    # print(count_mix)
    # list_dict_db = pd.DataFrame(count_mix)
    # list_dict_db=list_dict_db['raw_regexps']. tolist () # преобразовали столбец датафрейма в список регулярок словаря
    # print(list_dict_db)
    # list_dict_db.to_csv('C:\\Users\\piolv\\Desktop\\msm_koef_keys.csv')
    # return list_dict_db  # список регулярок отдельного словаря
    if name_type =='keys':
        with open("docs/key_tmp.txt", "r", encoding="utf-8") as file:
            # Read the lines into a list
            lines = file.readlines()
        # Strip newline characters from each line
        list_dict_db = [line.strip() for line in lines]
        return list_dict_db
    if name_type == 'exclusion':
        with open("docs/exc_tmp.txt", "r", encoding="utf-8") as file:
            # Read the lines into a list
            lines = file.readlines()
        # Strip newline characters from each line
        list_dict_db = [line.strip() for line in lines]
        print(list_dict_db, '-----')
        return list_dict_db

