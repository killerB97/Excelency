# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import xlwings as xw
import pandas as pd
import typing
from typing import Dict, Text, Any, List, Union, Optional, Tuple
from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
import webcolors
import xlsxwriter
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
        columns = tracker.get_slot('add_parameters')
        dest = tracker.get_slot('destination')
        pd_cols = columns[:]
        sheet1 = wbook.used_range.value
        df = pd.DataFrame(sheet1)
        previous_state = df.copy()
        if type(pd_cols)==str:
            column_list = df[self.colNameToNum(pd_cols)].sum(axis=0)
            wbook.range(dest).options(index=False, header=False, transpose=True).value = column_list
        else:
            column_list = []
            for i,n in enumerate(columns):
                pd_cols[i] = self.colNameToNum(n)
                column_list.append(pd_cols[i])
            column_list = df[column_list].sum(axis=1,  skipna = True, min_count=1).values
            wbook.range(dest+'1').options(index=False, header=False, transpose=True).value = column_list
        if len(columns)>1:
            dispatcher.utter_message(text="{} I have added the columns {} and {} for you and stored it in column {}".format(random.choice(start),''.join(columns[:-1]),columns[-1], dest))
        else:
            dispatcher.utter_message(text="{} I have added the columns {} for you and stored it in cell {}".format(random.choice(start),columns[0], dest))
        return [FollowupAction(name='action_restart')]

class ActionAddForm(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "add_info"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["parameters","destination"]

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        # utter submit template
        return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        
        return {
            "parameters": [self.from_entity(entity="parameters", intent='add'),self.from_entity(entity="parameters", intent=None)],
            "destination": [self.from_entity(entity="destination", intent=None),self.from_text(intent=None),]
        }
    
    def validate_parameters(self,
                 value: List,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:
        """Validate extracted requested slot
                else reject the execution of the form action
        """
        # extract other slots that were not requested
        # but set by corresponding entity
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        print(slot_values)
        # we'll check when validation failed in order
        # to add appropriate utterances
        if len(value)<1 or tracker.get_slot('add_parameters')!=None:
            return {"parameters":None}
        else:
            return {"parameters":value, "add_parameters":value}

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
        columns = tracker.get_slot('sort_parameters')
        flag = tracker.get_slot('pointer')

        if flag=='ascending':
            flag = True
        elif flag=='descending':
            flag=False
        else:
            flag=True

        pd_cols = self.colNameToNum(columns)
        sheet1 = wbook.used_range.value
        df = pd.DataFrame(sheet1)
        previous_state = df
        df = df.sort_values(by=pd_cols, ascending=flag)
        wbook.range(columns[0]+'1').options(index=False, header=False).value = df[pd_cols]
        dispatcher.utter_message(text="{} I have sorted the column {}".format(random.choice(start),columns))

        return [FollowupAction(name='action_restart')]

class ActionSortForm(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "sort_info"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["parameters","pointer"]

    def request_next_slot(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type: Dict[Text, Any]
    ):
        # type: (...) -> Optional[List[Dict]]
        """Request the next slot and utter template if needed,
            else return None"""

        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                if slot=='parameters':
                    dispatcher.utter_template(
                        "utter_ask_sort_parameters",
                        tracker,
                        silent_fail=False,
                        **tracker.slots
                    )
                else:
                    dispatcher.utter_template(
                        "utter_ask_{}".format(slot),
                        tracker,
                        silent_fail=False,
                        **tracker.slots
                    )
                return [SlotSet(REQUESTED_SLOT, slot)]

        # no more required slots to fill
        return None

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        # utter submit template
        return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        
        return {
            "parameters": [self.from_entity(entity="parameters", intent='sort'),self.from_entity(entity="parameters", intent=None)],
            "pointer": [self.from_entity(entity="pointer", intent=None),self.from_text(intent=None),]
        }
    
    def validate_parameters(self,
                 value: Text,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:
        """Validate extracted requested slot
                else reject the execution of the form action
        """
        # extract other slots that were not requested
        # but set by corresponding entity
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        print(slot_values)
        # we'll check when validation failed in order
        # to add appropriate utterances
        if len(value)<1 or tracker.get_slot('sort_parameters')!=None:
            return {"parameters":None}
        else:
            return {"parameters":value, "sort_parameters":value}

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

        return [FollowupAction(name='action_restart')]


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

        return [FollowupAction(name='action_restart')]


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

        return [FollowupAction(name='action_restart')]

class ActionMergeForm(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "merge_info"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["m_params","symbol"]

    def request_next_slot(
        self,
        dispatcher,  # type: CollectingDispatcher
        tracker,  # type: Tracker
        domain,  # type: Dict[Text, Any]
    ):
        # type: (...) -> Optional[List[Dict]]
        """Request the next slot and utter template if needed,
            else return None"""

        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                if slot=='m_params':
                    dispatcher.utter_template(
                        "utter_ask_merge_parameters",
                        tracker,
                        silent_fail=False,
                        **tracker.slots
                    )
                else:
                    dispatcher.utter_template(
                        "utter_ask_{}".format(slot),
                        tracker,
                        silent_fail=False,
                        **tracker.slots
                    )
                return [SlotSet(REQUESTED_SLOT, slot)]

        # no more required slots to fill
        return None

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        # utter submit template
        return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        
        return {
            "m_params": [self.from_entity(entity="m_params", intent='sort'),self.from_entity(entity="m_params", intent=None)],
            "symbol": [self.from_entity(entity="symbol", intent=None),self.from_text(intent=None),]
        }
    
    def validate_m_params(self,
                 value: List,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:
        """Validate extracted requested slot
                else reject the execution of the form action
        """
        # extract other slots that were not requested
        # but set by corresponding entity
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        print(slot_values)
        # we'll check when validation failed in order
        # to add appropriate utterances
        if len(value)<2 or tracker.get_slot('merge_parameters')!=None:
            return {"m_params":None}
        else:
            return {"m_params":value, "merge_parameters":value}

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

        return [FollowupAction(name='action_restart')]

class ActionColorCondition(Action):

    def name(self) -> Text:
        return "action_color_condition"

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
        axis = tracker.get_slot('axis')
        row_col = tracker.get_slot('parameters_cC')
        condition = tracker.get_slot('condition')
        color = tracker.get_slot('color')
        value= tracker.get_slot('value_cC')
        print(axis,row_col,condition,value)
        if condition and all(elem == "greater" for elem in condition):
            condition = '>'
        elif condition and all(elem in ("greater","equal") for elem in condition):
            condition = '>='
        elif condition and all(elem=="equal" for elem in condition):
            condition = '=='
        elif condition and all(elem=="lesser" for elem in condition):
            condition = '<'
        elif condition and all(elem in ("lesser","equal") for elem in condition):
            condition = '<='
        elif condition and all(elem=="between" for elem in condition):
            condition = '.between'
        elif condition and all(elem in ("greater","lesser") for elem in condition):
            condition = '.between'
        #Main color condition case everything given-
        if axis!=None and row_col!=None and condition!=None and  value!=None:
                if len(value)>1:
                    if value[0]>value[1]:
                        gr_value = '(value[1],value[0],inclusive=False)'
                    else:
                        gr_value = '(value[0],value[1],inclusive=False)'
                else:
                    gr_value = 'value[0]'

                if(axis=='rows'):
                    index = eval('df.loc[row_col,df.loc[row_col]'+condition+gr_value+'].index.tolist()')
                    try:
                        clr = webcolors.name_to_rgb(color) 
                    except:
                        clr = (255,255,255)
                    for i in index:
                        wbook.range(xlsxwriter.utility.xl_col_to_name(i)+str(int(row_col)+1)).color = clr

                elif(axis=='columns'):
                    index = eval('df[df[self.colNameToNum(row_col)]'+condition+gr_value+'].index.tolist()')
                    try:
                        clr = webcolors.name_to_rgb(color) 
                    except:
                        clr = (255,255,255)
                    for i in index:
                        wbook.range(row_col+str(i+1)).color = clr

        return [FollowupAction(name='action_restart')]

            #Yet to figure out how to handle a<=x<=b or a<=x<b or a<x<=b i.e. multiple instances of 'equal' in condition

        #Yet to create all other cases where everything is not given

