import json
import re
import pandas as pd

# количество повторяющихся регулярок
# s=pd.read_csv('C:\\tmp\sim_sui_prinyato.csv')
# s=s['all_tags']. tolist()

# def num_reg(s):
#     print(type(s), s)
#     kluchi_plus=[]
#     for i in s:
#         i = json.loads(i)
#         for a in i:
#             if re.fullmatch(r'\d\d\d', a['pattern']) == None and a['stop'] != True and a['machine_name']== 'narushenie_suicid':
#                 kluchi_plus.append(a['pattern'])
#     # print(len(kluchi_plus))
#     from collections import Counter
#     c = Counter(kluchi_plus).most_common()
#     #print(c)
#     print('-----------------')
#     tabl_reg=pd.DataFrame(c)
#     tabl_reg['stat_koef']=tabl_reg[1]/tabl_reg[1]. sum ()*100 #доля среди всех регулярок
#     print(tabl_reg)
#     return tabl_reg

def num_reg(s):
    s = s['all_tags']
    s = s.tolist()
    kluchi_plus=[]
    for i in s:
        i = json.loads(i)
        for a in i:
            if re.fullmatch(r'\d\d\d', a['pattern']) == None and a['stop'] != True and a['machine_name']== 'narushenie_suicid':
                kluchi_plus.append(a['pattern'])
    # print(len(kluchi_plus))
    from collections import Counter
    c = Counter(kluchi_plus).most_common()
    #print(c)
    print('-----------------')
    tabl_reg=pd.DataFrame(c)
    tabl_reg['stat_koef']=tabl_reg[1]/tabl_reg[1]. sum ()*100 #доля среди всех регулярок
    print(tabl_reg)
    return tabl_reg
