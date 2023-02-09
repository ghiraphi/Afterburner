# программа выводит список словарей из базы данных,
# отображая точность и количество регулярных выражений дл каждого словаря
# также отображается количество исключений на один ключ
# выводит данные в формате csv
# подсчёт точности по всем тематикам через бд
import pandas as pd
import psycopg2
from psycopg2 import Error
# SOURCES_SETTINGS = {
#     'user': '***',
#     'password': '***',
#     'host': '192.168.70.120',
#     'port': '5432',
#     'dbname': 'surmise'
# }
# try:
#     # Подключение к существующей базе данных
#     connection = psycopg2.connect(**SOURCES_SETTINGS)
#     cursor = connection.cursor()
#     print("Соединение началось")
#     # Курсор для выполнения операций с базой данных
#     cursor.execute(f"""
# with table0 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:иг"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '34') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# ),
# table1 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:масмб"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '104') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# ),
# table2 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:опрнасвл"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '148') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# ),
# table3 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:сосэ"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '105') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# ),
# table4 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:хт"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '33') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# ),
# table5 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='МСМ:ПС' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:ПС"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '32') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# ),
# table6 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:оскпр"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '149') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# ),
# table7 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:су"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '30') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# ),
# table8 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:cov"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '50') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# ),
# table9 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:qr"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '51') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# ),
# table10 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:сосзд"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '106') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# ),
# table11 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:яндспц"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '108') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# ),
# table12 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:консп"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '103') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# )
# ,
# table13 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:дпк"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '29') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# )
# ,
# table14 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:нар"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '31') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# )
# ,
# table15 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:прмб"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '112') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# )
# 	,
# table16 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:ич"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '47') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# )
# ,
# table17 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:ядв"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '107') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# )
# ,
# table18 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:мит"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '91') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# )
# ,
# table19 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:фк"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '98') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# )
# ,
# table20 as
# (
# SELECT
#    d,
#    CAST(COUNT(CASE WHEN status!='no_violations' THEN 0 END) AS FLOAT) /   COUNT(*) as "МСМ:митBr"
# FROM
#   generate_series('2022-01-01', '2022-12-31', interval '1 day') as gs(d)
#   left join surmise s
#   ON date_trunc('year', to_timestamp(s.created_at)) = gs.d
# where
# array_position(analysis_violations, '97') IS NOT NULL and
# is_manual = 'False'
# 	GROUP BY 1 ORDER BY 1
# )
#
# select table0.d , table0."МСМ:иг", table1."МСМ:масмб", table2."МСМ:опрнасв", table3."МСМ:сосэ", table4."МСМ:хт", table5."МСМ:ПС", table6."МСМ:оскпр", table7."МСМ:су", table8."МСМ:cov", table9."МСМ:qr", table10."МСМ:сосзд", table11."МСМ:яндспц", table12."МСМ:консп", table13."МСМ:дпк", table14."МСМ:нар", table15."МСМ:прмб", table16."МСМ:ич", table17."МСМ:ядв", table18."МСМ:мит", table19."МСМ:фк", table20."МСМ:митBr" from table0
# left  join table1 on table0.d = table1.d
# left  join table2 on table0.d = table2.d
# left  join table3 on table0.d = table3.d
# left  join table4 on table0.d = table4.d
# left  join table5 on table0.d = table5.d
# left  join table6 on table0.d = table6.d
# left  join table7 on table0.d = table7.d
# left  join table8 on table0.d = table8.d
# left  join table9 on table0.d = table9.d
# left  join table10 on table0.d = table10.d
# left  join table11 on table0.d = table11.d
# left  join table12 on table0.d = table12.d
# left  join table13 on table0.d = table13.d
# left  join table14 on table0.d = table14.d
# left  join table15 on table0.d = table15.d
# left  join table16 on table0.d = table16.d
# left  join table17 on table0.d = table17.d
# left  join table18 on table0.d = table18.d
# left  join table19 on table0.d = table19.d
# left  join table20 on table0.d = table20.d;
#
#     """)
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
#
# dat_stat = pd.DataFrame(count_mix)
# dat_stat.columns = ["Период", "МСМ:иг", "МСМ:масмбbr", "МСМ:опрнасвл", "МСМ:сосэbr", "МСМ:хт", "МСМ:ПС", "МСМ:оскпр", "МСМ:су", "МСМ:cov", "МСМ:qr", "МСМ:сосздbr",
#                     "МСМ:яндспц", "МСМ:конспbr", "МСМ:дпк", "МСМ:нар", "МСМ:прмб", "МСМ:ич", "МСМ:ядвbr", "МСМ:мит", "МСМ:фкbr", "МСМ:митBr"]
# # dat_stat.drop(labels = [1],axis = 0)
# dat_stat = dat_stat.T[2:]
# dat_stat.reset_index(inplace=True)
# print(dat_stat)
# dat_stat.to_csv('C:\\Users\\piolv\\Desktop\\msm_viol.csv')
#
#
# # подсчёт количества ключей и исключений в одном словаре
# SOURCES_SETTINGS = {
#     'user': '***',
#     'password': '***',
#     'host': '192.168.70.120',
#     'port': '5432',
#     'dbname': 'an_tags'
# }
#
# try:
#     # Подключение к существующей базе данных
#     connection = psycopg2.connect(**SOURCES_SETTINGS)
#     cursor = connection.cursor()
#     print("Соединение началось")
#     # Курсор для выполнения операций с базой данных
#     cursor.execute(f"""
#
# with table0 as (SELECT * FROM public.tag_handbook
# order by tag_id),
#
# table1 as (SELECT type as tip, handbook_id, LENGTH(REPLACE(raw_regexps, ':cs', ':cs*'))-LENGTH(raw_regexps) as dlina FROM public.dictionary
# where type='exclusion'),
#
# table2 as (SELECT id, violation_id, name FROM public.tag),
#
# table3 as (SELECT type as tip, handbook_id, LENGTH(REPLACE(raw_regexps, ':cs', ':cs*'))-LENGTH(raw_regexps) as dlina FROM public.dictionary
# where type='keyword'),
#
# table4 as (SELECT id, name, state, type FROM public.violation)
#
# select table4.id, table4.name, sum(table1.dlina) as exc_sum, sum(table3.dlina) as key_sum, sum(table1.dlina)::numeric/sum(table3.dlina) as koefic from table0
#     LEFT OUTER JOIN table1 ON (table0.handbook_id = table1.handbook_id)
#     LEFT OUTER JOIN table2 ON (table0.tag_id = table2.id)
# 	LEFT OUTER JOIN table3 ON (table0.handbook_id = table3.handbook_id)
# 	LEFT OUTER JOIN table4 ON (table2.violation_id = table4.id)
#
# where type='social_network' and
# state='working'
#
# group by 1,2
# order by 5 desc
#
#
#     """)
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
#
# koef = pd.DataFrame(count_mix)
# # dat_stat.drop(labels = [1],axis = 0)
# print(koef)
# koef.to_csv('C:\\Users\\piolv\\Desktop\\msm_koef_keys.csv')
#
#
# # объединение таблицы точности и количества регулярных выражений словарей

pd.options.display.max_columns = None # уже готовые датафреймы в качестве образца работоспособности программы
dat_stat = pd.read_csv('docs/msm_viol.csv')
print(dat_stat)
koef = pd.read_csv('docs/msm_koef_keys.csv')
#print(koef)
#print(dat_stat.columns.values.tolist())
#print(koef.columns.values.tolist())
list_dicts = pd.merge(dat_stat, koef, left_on='index', right_on='1') #фрейм со списком словарей
print(list_dicts)
list_dicts.to_csv('docs/res.csv')