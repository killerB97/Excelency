import pyttsx3

converter = pyttsx3.init()
converter.setProperty('rate', 150)
converter.setProperty('volume', 0.7)

converter.say ("Sure I will add a and b to c for you immediately")
#converter.setProperty('voice', voice_id)

#converter.runAndWait()

voices = converter.getProperty('voices')
#print (voices)


voice_id= 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'

converter.setProperty('voice', voice_id)

converter.runAndWait()


for voice in voices:
    # to get the info. about various voices in our PC
    print("Voice:")
    print("ID: %s" % voice.id)
    print("Name: %s" % voice.name)
    print("Age: %s" % voice.age)
    print("Gender: %s" % voice.gender)
    print("Languages Known: %s" % voice.languages)
