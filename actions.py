# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import xlwings as xw
import pandas as pd
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import random

start = ['Sure,', 'Certainly,', 'Absolutely,','Definitely,', 'For sure,']
previous_state = None

class ActionAddColumns(Action):

    def name(self) -> Text:
        return "action_add_columns"

    def colNameToNum(self,name):
        pow = 1
        colNum = 0
        for letter in name[::-1]:
                colNum += (int(letter, 36) -9) * pow
                pow *= 26
        return colNum-1

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global start
        global previous_state
        wbook = xw.Book('test.xlsx').sheets[0]
        columns = tracker.get_slot('parameters')
        dest = tracker.get_slot('destination')
        pd_cols = columns[:]
        for i,n in enumerate(columns):
            pd_cols[i] = self.colNameToNum(n) 
        sheet1 = wbook.used_range.value
        df = pd.DataFrame(sheet1)
        previous_state = df.copy()
        wbook.range(dest+'1').options(index=False, header=False, transpose=True).value = df[pd_cols[0]].values+df[pd_cols[1]].values
        dispatcher.utter_message(text="{} I have added the columns {} and {} for you and stored it in column {}".format(random.choice(start),columns[0],columns[1], dest))

        return []

class ActionSortColumns(Action):

    def name(self) -> Text:
        return "action_sort_columns"

    def colNameToNum(self,name):
        pow = 1
        colNum = 0
        for letter in name[::-1]:
                colNum += (int(letter, 36) -9) * pow
                pow *= 26
        return colNum-1

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global start
        global previous_state
        wbook = xw.Book('test.xlsx').sheets[0]
        columns = tracker.get_slot('parameters')
        flag = tracker.get_slot('pointer')

        if flag=='ascending':
            flag = True
        elif flag=='descending':
            flag=False
        else:
            flag=True

        pd_cols = columns[:]
        for i,n in enumerate(columns):
            pd_cols[i] = self.colNameToNum(n) 
        sheet1 = wbook.used_range.value
        df = pd.DataFrame(sheet1)
        previous_state = df
        df = df.sort_values(by=pd_cols[0], ascending=flag)
        wbook.range(columns[0]+'1').options(index=False, header=False).value = df[pd_cols[0]]
        dispatcher.utter_message(text="{} I have sorted the column {}".format(random.choice(start),columns[0]))

        return []

class ActionInsertColumns(Action):

    def name(self) -> Text:
        return "action_insert_columns"

    def colNameToNum(self,name):
        pow = 1
        colNum = 0
        for letter in name[::-1]:
                colNum += (int(letter, 36) -9) * pow
                pow *= 26
        return colNum-1

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global start
        global previous_state
        wbook = xw.Book('test.xlsx').sheets[0]
        columns = tracker.get_slot('parameters')
        pd_cols = columns[:]
        for i,n in enumerate(columns):
            pd_cols[i] = self.colNameToNum(n) 
        sheet1 = wbook.used_range.value
        df = pd.DataFrame(sheet1)
        previous_state = df
        wbook.api.columns[pd_cols[1]+1].insert_into_range()
        dispatcher.utter_message(text="{} I have inserted a column in between columns {} and {}".format(random.choice(start),columns[0],columns[1]))

        return []

class ActionDeleteColumns(Action):

    def name(self) -> Text:
        return "action_delete"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global start
        global previous_state
        wbook = xw.Book('test.xlsx').sheets[0]
        axis = tracker.get_slot('axis')
        param = tracker.get_slot('params')
        sheet1 = wbook.used_range.value
        df = pd.DataFrame(sheet1)
        previous_state = df.copy()
        if axis.lower() == 'rows' and param==None:
            wbook.clear_contents()
            df.dropna(how='all', inplace=True)
            wbook.range('A1').options(index=False, header=False,).value = df.values
            dispatcher.utter_message(text="{} I have deleted all empty rows".format(random.choice(start)))
        
        elif axis.lower() == 'columns' and param==None:
            wbook.clear_contents()
            df.dropna(axis=1, how='all', inplace=True)
            wbook.range('A1').options(index=False, header=False).value = df.values
            dispatcher.utter_message(text="{} I have deleted all empty columns".format(random.choice(start)))
        
        elif axis.lower() == 'columns':
            wbook.range(param[0]+':'+param[0]).api.delete()
            dispatcher.utter_message(text="{} I have deleted column {}".format(random.choice(start),param[0]))

        elif axis.lower() == 'rows':
            wbook.range(param[0]+':'+param[0]).api.delete()
            dispatcher.utter_message(text="{} I have deleted row {}".format(random.choice(start),param[0]))

        return [SlotSet("params", None)]


class ActionMergeColumns(Action):

    def name(self) -> Text:
        return "action_merge_columns"

    def colNameToNum(self,name):
        pow = 1
        colNum = 0
        for letter in name[::-1]:
                colNum += (int(letter, 36) -9) * pow
                pow *= 26
        return colNum-1

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global start
        global previous_state
        wbook = xw.Book('test.xlsx').sheets[0]
        columns = tracker.get_slot('m_params')
        delimiter = tracker.get_slot('symbol')
        if delimiter==None:
            delimiter=''
        pd_cols = columns[:]
        for i,n in enumerate(columns):
            pd_cols[i] = self.colNameToNum(n) 
        sheet1 = wbook.used_range.value
        df = pd.DataFrame(sheet1)
        previous_state = df
        wbook.range(columns[0]+'1').options(index=False, header=False, transpose=True).value  = df[[pd_cols[0], pd_cols[1]]].apply(lambda row: delimiter.join(row.values.astype(str)), axis=1).values 
        wbook.range(columns[1]+':'+columns[1]).api.clear_contents()
        dispatcher.utter_message(text="{} I have merged columns {} and {}".format(random.choice(start),columns[0],columns[1]))

        return []

class ActionUndo(Action):

    def name(self) -> Text:
        return "action_undo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global start
        global previous_state
        wbook = xw.Book('test.xlsx').sheets[0]
        wbook.clear_contents()
        wbook.range('A1').options(index=False, header=False).value = previous_state.values
        dispatcher.utter_message(text="{} I have managed to undo the previous change".format(random.choice(start)))

        return []