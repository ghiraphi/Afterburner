# программа фильтрует и затем сортирует словарь, который максимально подходит под условия обработки
# выводит номер словаря в переменную
import pandas as pd
import modules.accuracy_violance
tab= modules.accuracy_violance.list_dicts
# tab=pd.read_csv('C:\\Users\\piolv\\Desktop\\res.csv',  sep=',', encoding='utf8')
def filtr_dict_numb(tab):
    pd.options.display.max_rows = 1000
    pd.options.display.max_columns = 100
    pd.options.display.expand_frame_repr = False
    tab['otkl_sr_toch']=tab['0_x']/(tab['0_x']. sum()/ tab['0_x'].size)
    tab['otkl_sr_iskl']=tab['2']/(tab['2']. sum()/ tab['2'].size)
    tab['otkl_sr_sl']=tab['4']/(tab['4']. sum()/ tab['4'].size)
    tab['itog']=tab['otkl_sr_sl']+tab['otkl_sr_iskl']-tab['otkl_sr_toch']
    tab=tab.sort_values(by='itog', ascending=False)
    required_dictionary=tab.iloc [0]['0_y'] #номер словаря
    print(required_dictionary)
    return required_dictionary


