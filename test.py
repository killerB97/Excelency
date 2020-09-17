import xlwings as xw
import pandas as pd

def colNameToNum(name):
    pow = 1
    colNum = 0
    for letter in name[::-1]:
            colNum += (int(letter, 36) -9) * pow
            pow *= 26
    return colNum-1

wbook = xw.Book('test.xlsx').sheets[0]
#columns = tracker.get_slot('parameters')
columns = ['A', 'B']
pd_cols = columns[:]
for i,n in enumerate(columns):
    pd_cols[i] = colNameToNum(n) 
sheet1 = wbook.used_range.value
df = pd.DataFrame(sheet1)
wbook.range(columns[0]+'1').options(index=False, header=False, transpose=True).value  = df[[pd_cols[0], pd_cols[1]]].apply(lambda row: ' '.join(row.values.astype(str)), axis=1).values 
wbook.range(columns[1]+':'+columns[1]).api.clear_contents()
#dispatcher.utter_message(text="Sure I'll delete all empty columns")
