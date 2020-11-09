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
import matplotlib.colors as mcolors
import difflib
import xlsxwriter
import random

start = ['Sure,', 'Certainly,', 'Absolutely,','Definitely,', 'For sure,']
previous_state = None
previous_graph = None
format_state = None
format_color = []
format_cells = []
format_axis = None
selected_filename = None

class ActionFilename(Action):

    def name(self) -> Text:
        return "action_filename"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global selected_filename
        selected_filename=str(tracker.get_slot('filename'))

        return [FollowupAction(name='action_restart')]

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
        global start, previous_state, format_state, format_axis, format_cells, format_color,  selected_filename
        wbook = xw.Book(selected_filename).sheets[0]
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
        
        format_state = 'add'
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
        global start, previous_state, format_state, format_axis, format_cells, format_color, selected_filename
        wbook = xw.Book(selected_filename).sheets[0]
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

        format_state = 'sort'
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
        global start, previous_state, format_state, format_axis, format_cells, format_color,  selected_filename
        wbook = xw.Book(selected_filename).sheets[0]
        columns = tracker.get_slot('parameters')
        pd_cols = columns[:]
        for i,n in enumerate(columns):
            pd_cols[i] = self.colNameToNum(n) 
        sheet1 = wbook.used_range.value
        df = pd.DataFrame(sheet1)
        previous_state = df
        wbook.api.columns[pd_cols[1]+1].insert_into_range()
        dispatcher.utter_message(text="{} I have inserted a column in between columns {} and {}".format(random.choice(start),columns[0],columns[1]))

        format_state = 'insert'
        return [FollowupAction(name='action_restart')]


class ActionDeleteColumns(Action):

    def name(self) -> Text:
        return "action_delete"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global start, previous_state, format_state, format_axis, format_cells, format_color,  selected_filename
        wbook = xw.Book(selected_filename).sheets[0]
        axis = tracker.get_slot('axis')
        param = tracker.get_slot('parameters')
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

        format_state = 'delete'
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
        global start, previous_state, format_state, format_axis, format_cells, format_color,  selected_filename
        wbook = xw.Book(selected_filename).sheets[0]
        columns = tracker.get_slot('merge_parameters')
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

        format_state = 'merge'
        return [FollowupAction(name='action_restart')]

class ActionMergeForm(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "merge_info"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["parameters","symbol"]

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
            "parameters": [self.from_entity(entity="parameters", intent='merge'),self.from_entity(entity="parameters", intent=None)],
            "symbol": [self.from_entity(entity="symbol", intent=None),self.from_text(intent=None),]
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
        if len(value)<2 or tracker.get_slot('merge_parameters')!=None:
            return {"parameters":None}
        else:
            return {"parameters":value, "merge_parameters":value}

class ActionUndo(Action):

    def name(self) -> Text:
        return "action_undo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global start, previous_state, format_state, format_axis, format_cells, format_color,  selected_filename, previous_graph
        wbook = xw.Book(selected_filename).sheets[0]
        if format_state=='color':
            if(format_axis=='rows'):
                for n,i in enumerate(format_cells):
                    i.color = format_color[n]
            elif(format_axis=='columns'):
                for n,i in enumerate(format_cells):
                        i.color = format_color[n]

        if format_state=='graph':
            wbook.previous_graph.delete()

        elif format_state=='undo':
            dispatcher.utter_message(text="{} Sorry, I can only undo one change, no changes were made".format(random.choice(start)))
            return [FollowupAction(name='action_restart')]
        else:
            wbook.clear_contents()
            wbook.range('A1').options(index=False, header=False).value = previous_state.values

        dispatcher.utter_message(text="{} I have managed to undo the previous change".format(random.choice(start)))
        format_state='undo'
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
        global start, previous_state, format_state, format_axis, format_cells, format_color,  selected_filename
        wbook = xw.Book(selected_filename).sheets[0]
        axis = tracker.get_slot('axis')
        row_col = tracker.get_slot('parameters')[0]
        condition = tracker.get_slot('condition')
        color = tracker.get_slot('color')
        value= tracker.get_slot('value_cC')
        sheet1 = wbook.used_range.value
        df = pd.DataFrame(sheet1)
        previous_state = df.copy()
        print(axis,row_col,condition,value)
        if condition and all(elem == "greater" for elem in condition):
            condition = '>'
        elif set(condition)==set(['greater','equal']):
            condition = '>='
        elif condition and all(elem=="equal" for elem in condition):
            condition = '=='
        elif condition and all(elem=="lesser" for elem in condition):
            condition = '<'
        elif set(condition)==set(['lesser','equal']):
            condition = '<='
        elif condition and all(elem=="between" for elem in condition):
            condition = '.between'
        elif set(condition)==set(['greater','lesser']):
            condition = '.between'
        #Main color condition case everything given-
        if axis!=None and row_col!=None and condition!=None and  value!=None:
                if len(value)>1:
                    if int(value[0])>int(value[1]):
                        gr_value = '('+value[1]+','+value[0]+','+'inclusive=False)'
                    else:
                        gr_value = '('+value[0]+','+value[1]+','+'inclusive=False)'
                else:
                    gr_value = value[0]
                print(gr_value)
                if(axis=='rows'):
                    index = eval('df.loc[int(row_col)-1,df.loc[int(row_col)-1]'+condition+gr_value+'].index.tolist()')
                    try:
                        clr = webcolors.name_to_rgb(color) 
                        format_axis = 'rows'
                    except:
                        clr = (255,255,255)
                    for i in index:
                        cell = wbook.range(xlsxwriter.utility.xl_col_to_name(i)+str(int(row_col)))
                        format_cells.append(cell)
                        format_color.append(cell.color)
                        wbook.range(xlsxwriter.utility.xl_col_to_name(i)+str(int(row_col))).color = clr

                elif(axis=='columns'):
                    index = eval('df[df[self.colNameToNum(row_col)]'+condition+gr_value+'].index.tolist()')
                    try:
                        clr = webcolors.name_to_rgb(color) 
                        format_axis = 'columns'
                    except:
                        clr = (255,255,255)
                    for i in index:
                        cell = wbook.range(row_col+str(i+1))
                        format_cells.append(cell)
                        format_color.append(cell.color)
                        wbook.range(row_col+str(i+1)).color = clr

        dispatcher.utter_message(text="{} I have managed to color the appropriate cells".format(random.choice(start)))
        
        format_state = 'color'
        return [FollowupAction(name='action_restart')]

            #Yet to figure out how to handle a<=x<=b or a<=x<b or a<x<=b i.e. multiple instances of 'equal' in condition

        #Yet to create all other cases where everything is not given

class ActionColorForm(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "color_info"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["color"]

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
            "color": [self.from_entity(entity="color", intent=None),self.from_text(intent=None),]
        }
    
    def validate_color(self,
                 value: Text,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:
        """Validate extracted requested slot
                else reject the execution of the form action
        """
        # extract other slots that were not requested
        # but set by corresponding entity
        color_list = mcolors.CSS4_COLORS
        if value not in color_list.keys():
            value = difflib.get_close_matches(value,color_list.keys(),1)[0]
        # we'll check when validation failed in order
        # to add appropriate utterances
        return {"color": value}


class ActionGraphColumns(Action):

    def name(self) -> Text:
        return "action_graphs"

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
        global start, previous_state, format_state, format_axis, format_cells, format_color,  selected_filename, previous_graph
        cell_range = tracker.get_slot('parameters')
        graph_type = tracker.get_slot('graph_type')
        if cell_range==None:
            wbook = xw.Book(selected_filename).sheets[0]
            xlapp = xw.apps.active
            rng = xlapp.selection
            cells = rng.address.replace('$','')
        else:
            cells = ':'.join(cell_range)
        print(cells)
        df = xlapp.range(cells).options(pd.DataFrame, header=0, index=False).value
        if graph_type in ('bar','line'):
            ax = df.plot(kind=graph_type)
        else:
            ax = df.plot(kind=graph_type, x=df.columns[0], y= df.columns[1])
        fig = ax.get_figure()
        graph_object = wbook.pictures.add(fig, name='MyPlot', update=True,left=wbook.range(cells.split(':')[0]).left, top=wbook.range(cells.split(':')[0]).top)
        dispatcher.utter_message(text="{} I have merged columns {} and {}".format(random.choice(start),columns[0],columns[1]))
        format_state = 'graph'
        previous_graph = graph_object
        return [FollowupAction(name='action_restart')]


class ActionGraphForm(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "graph_info"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["parameters","graph_type"]

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
                        "utter_ask_graph_parameters",
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
            "parameters": [self.from_entity(entity="parameters", intent='graph'),self.from_entity(entity="parameters", intent=None)],
            "graph_type": [self.from_entity(entity="graph_type", intent=None),self.from_text(intent=None),]
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
        wbook = xw.Book(selected_filename).sheets[0]
        xlapp = xw.apps.active
        rng = xlapp.selection
        cells = rng.address.replace('$','')
        if len(value)<2 or tracker.get_slot('graph_parameters')!=None or cells==None:
            return {"parameters":None}
        else:
            return {"parameters":value, "graph_parameters":value}

    def validate_graph_type(self,
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
        if value not in ('line','bar','scatter'):
            return {"graph_type":None}
        else:
            return {"graph_type":value}
    