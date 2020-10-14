## happy path
* greet 
  - utter_greet 
* mood_great 
  - utter_happy 

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## add happy path
* greet
  - utter_greet
* add
  - add_info
  - form{"name": "add_info"}
  - form{"name": null}
  - action_add_columns
  - followup{"name": "action_restart"}
  - action_restart
  - action_listen


## add form stop
* greet
    - utter_greet
* add
    - add_info
    - form{"name": "add_info"}
* out_of_scope
    - utter_ask_continue
* deny
    - action_deactivate_form
    - form{"name": null}
    - utter_goodbye

## add survey continue
* greet
    - utter_greet
* add
    - add_info
    - form{"name": "add_info"}
* out_of_scope
    - utter_ask_continue
* affirm
    - add_info
    - form{"name": null}
    - action_add_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen

## out of scope
* out_of_scope
    - action_default_fallback

## restart
- action_restart
- action_listen


## add form
* add{"parameters": "H", "destination": "I"}
    - slot{"destination": "I"}
    - add_info
    - form{"name": "add_info"}
    - slot{"destination": "I"}
    - slot{"parameters": ["G", "H"]}
    - slot{"add_parameters": ["G", "H"]}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_add_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen
* add
    - add_info
    - form{"name": "add_info"}
    - slot{"parameters": ["G", "H"]}
    - slot{"add_parameters": ["G", "H"]}
    - slot{"requested_slot": "destination"}
* form: add{"parameters": "c"}
    - form: add_info
    - slot{"parameters": null}
    - slot{"destination": "c"}
    - slot{"requested_slot": "parameters"}
    - action_add_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen
* add{"destination": "K"}
    - slot{"destination": "K"}
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_goodbye

## add new path
* add{"destination": "I"}
    - slot{"destination": "I"}
    - add_info
    - form{"name": "add_info"}
    - slot{"destination": "I"}
    - slot{"destination": "I"}
    - slot{"requested_slot": "parameters"}
* form: add{"parameters": "L"}
    - form: add_info
    - slot{"parameters": ["J", "L"]}
    - slot{"add_parameters": ["J", "L"]}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_add_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen
* add{"parameters": "a"}
    - add_info
    - form{"name": "add_info"}
    - slot{"parameters": ["J", "L"]}
    - slot{"add_parameters": ["J", "L"]}
    - slot{"parameters": ["I", "a"]}
    - slot{"add_parameters": ["I", "a"]}
    - slot{"requested_slot": "destination"}
* form: add{"destination": "G"}
    - slot{"destination": "G"}
    - form: add_info
    - slot{"destination": "G"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_add_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen

## add new path 1
* add{"parameters": "C", "destination": "P"}
    - slot{"destination": "P"}
    - add_info
    - form{"name": "add_info"}
    - slot{"destination": "P"}
    - slot{"parameters": ["A", "B", "C"]}
    - slot{"destination": "P"}
    - slot{"add_parameters": ["A", "B", "C"]}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_add_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen
* add{"parameters": "G", "destination": "M7"}
    - slot{"destination": "M7"}
    - add_info
    - form{"name": "add_info"}
    - slot{"parameters": ["A", "B", "C"]}
    - slot{"destination": "M7"}
    - slot{"add_parameters": ["A", "B", "C"]}
    - slot{"parameters": "G"}
    - slot{"destination": "M7"}
    - slot{"add_parameters": "G"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_add_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen
* add
    - add_info
    - form{"name": "add_info"}
    - slot{"parameters": null}
    - slot{"destination": "M7"}
    - slot{"requested_slot": "parameters"}
* out_of_scope
    - utter_ask_continue
* deny
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}
    - utter_goodbye

## sort happy path
* greet
  - utter_greet
* sort
  - sort_info
  - form{"name": "sort_info"}
  - form{"name": null}
  - action_sort_columns
  - followup{"name": "action_restart"}
  - action_restart
  - action_listen

## sort form stop
* greet
    - utter_greet
* sort
    - sort_info
    - form{"name": "sort_info"}
* out_of_scope
    - utter_ask_continue
* deny
    - action_deactivate_form
    - form{"name": null}
    - utter_goodbye

## sort survey continue
* greet
    - utter_greet
* sort
    - sort_info
    - form{"name": "sort_info"}
* out_of_scope
    - utter_ask_continue
* affirm
    - sort_info
    - form{"name": null}
    - action_sort_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen


## insert happy path
* sort
  - action_insert_columns
  - followup{"name": "action_restart"}
  - action_restart
  - action_listen

## delete happy path
* delete
  - action_delete
  - followup{"name": "action_restart"}
  - action_restart
  - action_listen


## fallback
- action_default_fallback

## undo happy path
* undo
  - action_undo
  - followup{"name": "action_restart"}
  - action_restart
  - action_listen



## add long path
* add{"parameters": "I", "destination": "F"}
    - slot{"destination": "F"}
    - add_info
    - form{"name": "add_info"}
    - slot{"destination": "F"}
    - slot{"parameters": ["D", "G", "I"]}
    - slot{"destination": "F"}
    - slot{"add_parameters": ["D", "G", "I"]}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_add_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen
* add{"parameters": "F", "destination": "G12"}
    - slot{"destination": "G12"}
    - add_info
    - form{"name": "add_info"}
    - slot{"parameters": ["D", "G", "I"]}
    - slot{"destination": "G12"}
    - slot{"add_parameters": ["D", "G", "I"]}
    - slot{"parameters": "F"}
    - slot{"destination": "G12"}
    - slot{"add_parameters": "F"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_add_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen
* add{"parameters": "D", "destination": "b9"}
    - slot{"destination": "b9"}
    - add_info
    - form{"name": "add_info"}
    - slot{"parameters": "F"}
    - slot{"destination": "b9"}
    - slot{"add_parameters": "F"}
    - slot{"parameters": "D"}
    - slot{"destination": "b9"}
    - slot{"add_parameters": "D"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_add_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen
* add{"parameters": "B", "destination": "i7"}
    - slot{"destination": "i7"}
    - add_info
    - form{"name": "add_info"}
    - slot{"parameters": "D"}
    - slot{"destination": "i7"}
    - slot{"add_parameters": "D"}
    - slot{"parameters": "B"}
    - slot{"destination": "i7"}
    - slot{"add_parameters": "B"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_add_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen
* add{"parameters": "E", "destination": "h22"}
    - slot{"destination": "h22"}
    - add_info
    - form{"name": "add_info"}
    - slot{"parameters": "B"}
    - slot{"destination": "h22"}
    - slot{"add_parameters": "B"}
    - slot{"parameters": "E"}
    - slot{"destination": "h22"}
    - slot{"add_parameters": "E"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_add_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen

## sort long path
* sort
    - sort_info
    - form{"name": "sort_info"}
    - slot{"requested_slot": "parameters"}
* form: add{"parameters": "B"}
    - form: sort_info
    - slot{"parameters": "B"}
    - slot{"sort_parameters": "B"}
    - slot{"requested_slot": "pointer"}
* form: sort{"pointer": "ascending"}
    - slot{"pointer": "ascending"}
    - form: sort_info
    - slot{"pointer": "ascending"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_sort_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen
* sort{"parameters": "a"}
    - sort_info
    - form{"name": "sort_info"}
    - slot{"parameters": "B"}
    - slot{"sort_parameters": "B"}
    - slot{"parameters": "a"}
    - slot{"sort_parameters": "a"}
    - slot{"requested_slot": "pointer"}
* form: sort{"pointer": "descending"}
    - slot{"pointer": "descending"}
    - form: sort_info
    - slot{"pointer": "descending"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_sort_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen

## merge happy path
* greet
  - utter_greet
* merge
  - merge_info
  - form{"name": "merge_info"}
  - form{"name": null}
  - action_merge_columns
  - followup{"name": "action_restart"}
  - action_restart
  - action_listen

## merge form stop
* greet
    - utter_greet
* merge
    - merge_info
    - form{"name": "merge_info"}
* out_of_scope
    - utter_ask_continue
* deny
    - action_deactivate_form
    - form{"name": null}
    - utter_goodbye

## merge survey continue
* greet
    - utter_greet
* merge
    - merge_info
    - form{"name": "merge_info"}
* out_of_scope
    - utter_ask_continue
* affirm
    - merge_info
    - form{"name": null}
    - action_merge_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen


## merge long path
* merge{"m_params": "B"}
    - slot{"m_params": "B"}
    - merge_info
    - form{"name": "merge_info"}
    - slot{"m_params": null}
    - slot{"m_params": ["A", "B"]}
    - slot{"merge_parameters": ["A", "B"]}
    - slot{"requested_slot": "symbol"}
* form: merge
    - form: merge_info
    - slot{"symbol": "*"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_merge_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen
* merge{"m_params": "D"}
    - slot{"m_params": "D"}
    - merge_info
    - form{"name": "merge_info"}
    - slot{"m_params": null}
    - slot{"m_params": null}
    - slot{"requested_slot": "m_params"}
* form: merge{"m_params": "E"}
    - slot{"m_params": "E"}
    - form: merge_info
    - slot{"m_params": ["D", "E"]}
    - slot{"merge_parameters": ["D", "E"]}
    - slot{"requested_slot": "symbol"}
* form: deny
    - form: merge_info
    - slot{"symbol": "$"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_merge_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen


## restart add
* add{"parameters": "B", "destination": "C"}
    - slot{"destination": "C"}
    - add_info
    - form{"name": "add_info"}
    - slot{"destination": "C"}
    - slot{"parameters": ["A", "B"]}
    - slot{"destination": "C"}
    - slot{"add_parameters": ["A", "B"]}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_add_columns
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen

## color fill restart 1
* color_condition{"axis": "rows", "parameters_cC": "3", "condition": "equal", "value_cC": "76"}
    - slot{"axis": "rows"}
    - slot{"condition": ["equal"]}
    - slot{"parameters_cC": ["3"]}
    - slot{"value_cC": ["76"]}
    - utter_ask_color
* color_condition{"color": "gray"}
    - slot{"color": "gray"}
    - action_color_condition
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen

## color fill restart 2
* color_condition{"axis": "columns", "parameters_cC": "E", "condition": "between", "value_cC": "20"}
    - slot{"axis": "columns"}
    - slot{"condition": ["between"]}
    - slot{"parameters_cC": ["E"]}
    - slot{"value_cC": ["5", "20"]}
    - utter_ask_color
* color_condition{"color": "green"}
    - slot{"color": "green"}
    - action_color_condition
    - followup{"name": "action_restart"}
    - action_restart
    - action_listen

## interactive_story_1
* color_condition{"color": "pink", "axis": "columns", "parameters_cC": "G", "condition": "lesser", "value_cC": "100"}
    - slot{"axis": "columns"}
    - slot{"color": "pink"}
    - slot{"condition": ["lesser"]}
    - slot{"parameters_cC": ["G"]}
    - slot{"value_cC": ["100"]}
    - action_color_condition
    - followup{"name": "action_restart"}
    - action_restart


## add happy path
* greet
  - utter_greet
* color_condition
  - color_info
  - form{"name": "color_info"}
  - form{"name": null}
  - action_color_condition
  - followup{"name": "action_restart"}
  - action_restart
  - action_listen
