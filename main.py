import modules.accuracy_violance
import modules.choose_dict
import modules.find_plus_minus
import modules.num_repeat_reg
import modules.ineffecive_keys_simpoma
import modules.delete_regular
import modules.get_reg_db
import modules.record_reg


numb_viol= modules.choose_dict.filtr_dict_numb(modules.accuracy_violance.list_dicts) #выбран номер темы для работы
print(numb_viol, 'номер темы для работы')
plus= modules.find_plus_minus.find_regs(2, numb_viol) #список материалов по тегу, принятые материалы и их ключи
minus= modules.find_plus_minus.find_regs(3, numb_viol) #список материалов по тегу, отклонённые материалы и их ключи

list_key= modules.get_reg_db.get_list_reg('keys', numb_viol) #исходный список ключей из дб
list_exc= modules.get_reg_db.get_list_reg('exclusion', numb_viol) #исходный список исключений из дб
#git rm -r --cached .
tabl_prin= modules.num_repeat_reg.num_reg(plus) #таблица с количеством повторяющихся регулярок в принятых материалах
tabl_otkl= modules.num_repeat_reg.num_reg(minus) #таблица с количеством повторяющихся регулярок в отклонённых материалах

list_new_keys= modules.ineffecive_keys_simpoma.del_keys(tabl_prin, tabl_otkl)  #список новых ключей после сокращения по фильтру
#
new_keys= modules.delete_regular.del_reg(list_new_keys) #список новых ключей после сокращения дублей регулярок
new_exc= modules.delete_regular.del_reg(list_exc)  #новый итоговый список исключений


#
modules.record_reg.rec_reg_db(new_keys, 'keys', numb_viol) #запись в базу данных новых ключей
modules.record_reg.rec_reg_db(new_exc, 'exclusion', numb_viol) #запись в базу данных новых исключений

print(f'всего в словаре:\nбыло- {len(list_key)+len(list_exc)}\nосталось- {len(new_keys)+len(new_exc)}')
