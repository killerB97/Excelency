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
  -  action_add_columns


## add long path
* greet
    - utter_greet
* add{"parameters": "B", "destination": "D"}
    - slot{"destination": "D"}
    - slot{"parameters": ["A", "B"]}
    - action_add_columns
* add{"destination": "H"}
    - slot{"destination": "H"}
    - action_add_columns
* add{"destination": "I"}
    - slot{"destination": "I"}
    - action_add_columns
* add{"parameters": "C"}
    - slot{"parameters": ["A", "C"]}
    - utter_ask_destination
* add{"destination": "J"}
    - slot{"destination": "J"}
    - action_add_columns
* add{"parameters": "G", "destination": "K"}
    - slot{"destination": "K"}
    - slot{"parameters": ["G"]}
    - utter_ask_columns
* add{"parameters": "F", "destination": "K"}
    - slot{"destination": "K"}
    - slot{"parameters": ["G", "F"]}
    - action_add_columns
* grateful
    - utter_happy

## add missing destination path
* greet
    - utter_greet
* add{"parameters": "B"}
    - slot{"parameters": ["A", "B"]}
    - utter_ask_destination
* add{"destination": "K"}
    - slot{"destination": "K"}
    - action_add_columns
* add{"destination": "D"}
    - slot{"destination": "D"}
    - action_add_columns

## add missing columns path 
* greet
    - utter_greet
* add{"parameters": "B", "destination": "C"}
    - slot{"destination": "C"}
    - slot{"parameters": ["B"]}
    - utter_ask_columns
* add{"parameters": "A", "destination": "C"}
    - slot{"destination": "C"}
    - slot{"parameters": ["B", "A"]}
    - action_add_columns
* grateful
    - utter_happy
* add{"destination": "H"}
    - slot{"destination": "H"}
    - utter_ask_columns
* add{"parameters": "G", "destination": "H"}
    - slot{"destination": "H"}
    - slot{"parameters": ["F", "G"]}
    - action_add_columns
* grateful
    - utter_happy
* add{"destination": "E"}
    - slot{"destination": "E"}
    - action_add_columns
* goodbye
    - utter_goodbye

## add mixed columns path
* greet
    - utter_greet
* add{"parameters": "B", "destination": "D"}
    - slot{"destination": "D"}
    - slot{"parameters": ["A", "B"]}
    - action_add_columns
* add{"destination": "I"}
    - slot{"destination": "I"}
    - action_add_columns
* add{"destination": "K"}
    - slot{"destination": "K"}
    - action_add_columns
* add{"destination": "E"}
    - slot{"destination": "E"}
    - utter_ask_columns
* add{"parameters": "B", "destination": "E"}
    - slot{"destination": "E"}
    - slot{"parameters": ["A", "B"]}
    - action_add_columns
* grateful
    - utter_happy


## add mixed destination path
* add{"parameters": "G"}
    - slot{"parameters": ["F", "G"]}
    - utter_ask_destination
* add{"destination": "K"}
    - slot{"destination": "K"}
    - action_add_columns
* add{"parameters": "K"}
    - slot{"parameters": ["G", "K"]}
    - utter_ask_destination
* add{"destination": "H"}
    - slot{"destination": "H"}
    - action_add_columns
* grateful
    - utter_happy

## add missing destination columns path
* add{"parameters": "F"}
    - slot{"parameters": ["F"]}
    - utter_ask_columns
* add{"parameters": "G"}
    - slot{"parameters": ["F", "G"]}
    - utter_ask_destination
* add{"destination": "C"}
    - slot{"destination": "C"}
    - action_add_columns
* grateful
    - utter_happy

## sort happy path
* greet
  - utter_greet
* sort
  -  action_sort_columns


## sort missing pointer
* greet
    - utter_greet
* sort{"parameters": "G", "pointer": "ascending"}
    - slot{"parameters": ["G"]}
    - slot{"pointer": "ascending"}
    - action_sort_columns
* sort{"parameters": "B"}
    - slot{"parameters": ["B"]}
    - utter_ask_pointer
* sort{"pointer": "descending"}
    - slot{"pointer": "descending"}
    - action_sort_columns

## sort missing columns
* greet
    - utter_greet
* sort{"pointer": "descending"}
    - slot{"pointer": "descending"}
    - utter_ask_columns
* add{"parameters": "I"}
    - slot{"parameters": ["I"]}
    - action_sort_columns
* grateful
    - utter_happy

## sort missing columns pointer
* sort
    - utter_ask_columns
* add{"parameters": "B"}
    - slot{"parameters": ["B"]}
    - utter_ask_pointer
* sort{"pointer": "ascending"}
    - slot{"pointer": "ascending"}
    - action_sort_columns

## insert happy path
* greet
  - utter_greet
* sort
  -  action_insert_columns

## insert missing column 1 path
* greet
    - utter_greet
* insert{"parameters": "B"}
    - slot{"parameters": ["A", "B"]}
    - action_insert_columns
* grateful
    - utter_happy

## insert missing column 2 path
* insert{"parameters": "D"}
    - slot{"parameters": ["D"]}
    - utter_ask_columns
* insert{"parameters": "E"}
    - slot{"parameters": ["D", "E"]}
    - action_insert_columns

## insert missing both path
* insert
    - utter_ask_columns
* insert{"parameters": "J"}
    - slot{"parameters": ["I", "J"]}
    - action_insert_columns
* grateful
    - utter_happy



## mixed add insert sort path
* add{"parameters": "B", "destination": "C"}
    - slot{"destination": "C"}
    - slot{"parameters": ["A", "B"]}
    - action_add_columns
* insert{"parameters": "C"}
    - slot{"parameters": ["B", "C"]}
    - action_insert_columns
* sort{"parameters": "B"}
    - slot{"parameters": ["B"]}
    - utter_ask_pointer
* sort{"pointer": "descending"}
    - slot{"pointer": "descending"}
    - action_sort_columns


## interactive_story_1
* add{"parameters": "B", "destination": "C"}
    - slot{"destination": "C"}
    - slot{"parameters": ["A", "B"]}
    - action_add_columns
* add{"destination": "F"}
    - slot{"destination": "F"}
    - action_add_columns
* sort{"parameters": "F", "pointer": "ascending"}
    - slot{"parameters": ["F"]}
    - slot{"pointer": "ascending"}
    - action_sort_columns
* sort{"pointer": "descending"}
    - slot{"pointer": "descending"}
    - action_sort_columns
