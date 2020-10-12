import flask
from flask import Flask,request, Response, jsonify, make_response
import numpy as np
from flask import send_file 
import speech_recognition as sr  

app = Flask(__name__)

@app.route('/speech', methods= ['POST','GET'])
def post():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:  # mention source it will be either Microphone or audio files.
            audio = r.listen(source,timeout=7.0)
            message = r.recognize_google(audio)
        except:
            message = ''  # use recognizer to convert our audio into text part.
    return jsonify({'stt':message})



if __name__ == "__main__":
    app.run(host='localhost', debug=True)