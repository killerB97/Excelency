## Run this command in terminal  before executing this program
## rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
## and also run this in seperate terminal
## rasa run actions

import requests
import speech_recognition as sr     # import the library
import subprocess
from gtts import gTTS
from mpyg321.mpyg321 import MPyg321Player


player = MPyg321Player()

# sender = input("What is your name?\n")

bot_message = ""
message=""

print('Welcome to the chatbot')

r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": "Hello"})

print("Lency: ",end=' ')
for i in r.json():
    bot_message = i['text']
    print(f"{bot_message}")

myobj = gTTS(text=bot_message)
myobj.save("welcome.mp3")
# Playing the converted file
player.play_song("/Users/raji/Chatbot/welcome.mp3")

while bot_message != "Bye" or bot_message!='thanks':

    r = sr.Recognizer()  # initialize recognizer
    with sr.Microphone() as source:  # mention source it will be either Microphone or audio files.
        print("Speak Anything :")
        audio = r.listen(source)  # listen to the source
        try:
            message = r.recognize_google(audio)  # use recognizer to convert our audio into text part.
            print("User: {}".format(message))

        except:
            print("Sorry could not recognize your voice")  # In case of voice not recognized  clearly
    if len(message)==0:
        continue

    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})

    print("Lency: ",end=' ')
    for i in r.json():
        bot_message = i['text']
        print(f"{bot_message}")

    myobj = gTTS(text=bot_message)
    myobj.save("welcome.mp3")
    # Playing the converted file
    player.play_song("/Users/raji/Chatbot/welcome.mp3")

    a = input('click Enter:')