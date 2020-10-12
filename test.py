import xlwings as xw
import pandas as pd
import webcolors
import xlsxwriter

def colNameToNum(name):
    pow = 1
    colNum = 0
    for letter in name[::-1]:
            colNum += (int(letter, 36) -9) * pow
            pow *= 26
    return colNum-1

wbook = xw.Book('test.xlsx').sheets[0]
#columns = tracker.get_slot('add_parameters')
#dest = tracker.get_slot('destination')
columns = ['E','D']
dest = 'H'
pd_cols = columns[:]
sheet1 = wbook.used_range.value
df = pd.DataFrame(sheet1)
apple = '(30,70, inclusive=False)'
index = eval('df.loc[3,df.loc[3].between'+apple+'].index.tolist()')
#index = df[df[3]>30].index.tolist() 
clr = webcolors.name_to_rgb('yellow')
for i in index:
    wbook.range(xlsxwriter.utility.xl_col_to_name(i)+'4').color = clr
    #wbook.range('D'+str(i+1)).color = clr
#dispatcher.utter_message(text="Sure I'll delete all empty columns"
