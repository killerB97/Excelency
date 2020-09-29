## intent:greet
- hey
- hello
- hi
- good morning
- good evening
- hey there
- Hi there
- Hi
- Hello
- hi there
- hello there

## intent:goodbye
- bye
- goodbye
- see you around
- see you later
- See you later

## intent:add
- Can you please add the two columns [A](parameters) and [B](parameters) and store it in [C](destination)
- Add the columns [B](parameters) and [C](parameters) please and put it in [K](destination)
- Please sum column [E](parameters) and column [K](parameters) and place it in [F](destination)
- Give me the sum of columns [F](parameters) and [I](parameters) and add to column [T](destination)
- sum column [T](parameters) and [G](parameters) to [G](destination)
- find the total of column [A](parameters) and column [B](parameters) and shift to [N](destination)
- Find the sum of [A](parameters) and [C](parameters) as well as store in [R](destination)
- add up column [F](parameters) and [I](parameters) and send to column [D](destination)
- Please find the addition of [D](parameters) and [Y](parameters) to column [S](destination)
- Add [R](parameters) and [J](parameters) and add to column [I](destination)
- Can you please sum column [A](parameters) and [B](parameters) to [D](destination)
- Can you again add the columns and put in [H](destination)
- can you please add them again to [I](destination)
- Can you add [A](parameters) and [C](parameters)
- yes please add to [J](destination)
- can you please add [G](parameters) to [K](destination)
- can you please add [G](parameters) and [F](parameters) to [K](destination)
- Can you add [A](parameters) and [B](parameters)
- Yes please add to [K](destination)
- Can you add them again to [D](destination) instead now
- Can you add column [B](parameters) to [C](destination)
- Yes can you add [B](parameters) and [A](parameters) to [C](destination)
- can you add and store to column [H](destination)
- Oh sorry can you add [F](parameters) and [G](parameters) to [H](destination)
- can you add them again to [E](destination) instead
- Can you add [A](parameters) and [B](parameters) to [D](destination)
- Can you add them again to [I](destination) instead
- can you add them again to [K](destination)
- can you add the columns to [E](destination)
- My bad please add the coulms [A](parameters) and [B](parameters) to [E](destination)
- Can you please add [F](parameters) and [G](parameters) please
- Yes please add them to [K](destination)
- sum up [G](parameters) and [K](parameters)
- Oh yes put it in [H](destination)
- total column [F](parameters) please
- sum up [F](parameters) and [G](parameters)
- total them and put in [C](destination)
- sum up [A](parameters) and [B](parameters) and store in [C](destination)
- Can you add column [A](parameters) and [B](parameters) and store it in [C](destination)
- can you add [A](parameters) and [B](parameters) to [C](destination)
- can you add them again to [F](destination) instead
- can you add column [A](parameters) and [B](parameters) to [C](destination)
- can you add [A](parameters) and [b](parameters) to [C](destination)
- add column [B](parameters) and column [C](parameters) to [G](destination)
- add column [a](parameters) and [B](parameters) to [G](destination)
- add [a](parameters) and [b](parameters) to [G](destination)
- total columns [A](parameters) and [B](parameters) and store in [F](destination)
- sum up [A](parameters) and [B](parameters) to [C](parameters) please
- add [A](parameters) and [B](parameters) to [C](destination) please
- sum up [B](parameters) and [c](parameters)
- [G](destination)
- add [A](parameters) and [B](parameters) to [I](destination)
- can you add [d](parameters) and [e](parameters) to [J](destination)
- add [D](parameters) and [e](parameters) to [h](destination)

## intent:sort
- can you sort column [B](parameters) in [ascending](pointer) order
- sort [C](parameters) in [descending](pointer) order
- please sort [A](parameters) in [ascending](pointer)
- sort column [H](parameters) in [descending](pointer) please
- can you arrange column [E](parameters) in [ascending](pointer) order please
- arrange column [F](parameters) in [descending](pointer) order please
- take column [G](parameters) and sort it in [ascending](pointer) order
- sort column [I](parameters)
- make [J](parameters) sorted
- Can you sort column [G](parameters) in [ascending](pointer) order for me
- sort [B](parameters)
- [descending](pointer)
- sort the column in [descending](pointer) order
- Can you sort the column
- [ascending](pointer)
- yes column [I](parameters)
- Yes [B](parameters) please
- please arrange column [B](parameters)
- [descending](pointer) order
- please arrange column [F](parameters) in [ascending](pointer) order
- can you srt the column again in [descending](pointer) order
- also sort [C](destination)
- short column [g](parameters)
- short [F](parameters)

## intent:insert
- Can you insert a column in between [B](parameters) and [C](parameters)
- Please add a column in between [G](parameters) and [H](parameters)
- insert column between [D](parameters) and [E](parameters) please
- insert between [F](parameters) and [G](parameters)
- add between [M](parameters) and [N](parameters)
- place column in between [A](parameters) and [B](parameters)
- please put column in between [S](parameters) and [T](parameters)
- Can you insert column between [A](parameters) and [B](parameters)
- Can you add column between [D](parameters)
- Oh sorry between [D](parameters) and [E](parameters)
- Can you put a column
- Yes please put it in between [I](parameters) and [J](parameters)
- can you insert a column in between [B](parameters) and [C](parameters)
- insert column between [E](parameters) and [F](parameters)
- please insert column between [B](parameters) and [C](parameters)
- insert a column on [c](destination)
- insert a column in between [B](parameters) and [C](parameters)

## intent:delete
- delete all empty [rows](axis)
- delete all empty [row](axis)
- remove all empty [horizontals](axis)
- clear all empty [cols](axis)
- remove empty [columns](axis)
- delete empty [col](axis)
- clear empty [row](axis)
- get rid of all empty [verticals](axis)
- get rid of empty [rows](axis)
- clear out empty [column](axis)
- delete [row](axis) [5](params)
- remove [col](axis) [J](params)
- clear [column](axis) [I](params)
- get rid of [row](axis) [8](params)
- delete [cols](axis) [A](params)
- can you delete all empty [rows](axis)
- can you delete [column]{"entity": "axis", "value": "columns"} [B](params)
- remove all empty [columns](axis)
- clear [row]{"entity": "axis", "value": "rows"} [2](params)
- remove [row]{"entity": "axis", "value": "rows"} [3](params)
- clear [column]{"entity": "axis", "value": "columns"} [c](params)
- please delete [column]{"entity": "axis", "value": "columns"} [B](params)
- can you delete [column]{"entity": "axis", "value": "columns"} [D](params)
- delete [column]{"entity": "axis", "value": "columns"} [G](params) please
- delete all empty [columns](axis)
- clear [col]{"entity": "axis", "value": "columns"} [C](params)
- delete [column]{"entity": "axis", "value": "columns"} [f](params)
- delete [column]{"entity": "axis", "value": "columns"} [j](params)
- delete [row]{"entity": "axis", "value": "rows"} [3](params)

## intent:merge
- please merge columns [c](m_params) and [d] {"entity":"m_params", "role": "second"}
- can you merge columns [A](m_params) and [e] {"entity":"m_params", "role": "second"}
- merge [F](m_params) and [J] {"entity":"m_params", "role": "second"}
- please combine [S](m_params) and [t] {"entity":"m_params", "role": "second"}
- combine cols [k](m_params) and [d] {"entity":"m_params", "role": "second"}
- merge the columns [G](m_params) and [H] {"entity":"m_params", "role": "second"}
- can you merge column [C](m_params) and [D]{"entity": "m_params", "role": "second"}
- [+](symbol)
- [-](symbol)
- [/](symbol)
- merge column [D](m_params) and [e]{"entity": "m_params", "role": "second"}
- [:](symbol)

## intent:undo
- can you please undo the last function
- please undo
- undo
- revert back to the previous state
- revert the changes
- undo the change
- please undo that
- undo please
- undo that please

## intent:affirm
- yes
- indeed
- of course
- that sounds good
- correct

## intent:deny
- no
- never
- I don't think so
- don't like that
- no way
- not really

## intent:mood_great
- perfect
- very good
- great
- amazing
- wonderful
- I am feeling very good
- I am great
- I'm good

## intent:grateful
- Thank you
- This was very helpful
- Thanks a ton
- Thanks for the help
- you have been very helpful
- This is great
- Thanks a lot
- you are awesome
- Thank you that was great
- thank you
- thanks a lot
- thanks this was super helpful

## intent:mood_unhappy
- sad
- very sad
- unhappy
- bad
- very bad
- awful
- terrible
- not very good
- extremely sad
- so sad

## intent:bot_challenge
- are you a bot?
- are you a human?
- am I talking to a bot?
- am I talking to a human?
- who are you
- who is this

## synonym:columns
- column
- col
- cols
- verticals

## synonym:rows
- row
- sequence
- horizontals
