import speech_recognition as sr

r1 = sr.Recognizer()

with sr.Microphone() as source:
    audio = r1.listen(source)

print(r1.recognize_google(audio))


