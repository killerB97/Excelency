import xlwings as xw
import pandas as pd
import webcolors
import xlsxwriter
import difflib
import matplotlib.colors as mcolors
import pandas as pd

def colNameToNum(name):
    pow = 1
    colNum = 0
    for letter in name[::-1]:
            colNum += (int(letter, 36) -9) * pow
            pow *= 26
    return colNum-1


wbook = xw.Book('test.xlsx').sheets[0]
copy = xw.Book('test.xlsx').sheets[0]
xlapp = xw.apps.active
rng = xlapp.selection
cells = rng.address.replace('$','')
print(cells)
'''df = xlapp.range(cells).options(pd.DataFrame, header=0, index=False).value
ax = df.plot(kind='scatter', x=df.columns[0],y=df.columns[1])
fig = ax.get_figure()
graph_object = wbook.pictures.add(fig, name='MyPlot', update=True,left=wbook.range(cells.split(':')[0]).left, top=wbook.range(cells.split(':')[0]).top)'''
