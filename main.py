import os
import speech_recognition as sr
import gtts
from playsound import playsound
from datetime import datetime

from notion import create_page

r= sr.Recognizer()


ACTIVATION_COMMAND = "hello"
def get_audio():
    with sr.Microphone() as source: 
        print("Say activation key")
        audio = r.listen(source)
    return audio

def audio_to_text(audio):
    text= ""
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError: 
        print("Speech Recognition could not recognize")
    except sr.RequestError: 
        print("Could not request from API")
    return text


def play_sound(text):
    try:
        tts = gtts.gTTS(text)
        audio_file = os.path.dirname(__file__) + 'audio.mp3'
        tts.save(audio_file)
        playsound(audio_file)
        os.remove(audio_file) 
    except AssertionError:
        print("Could not play the sound")
        
if __name__ == "__main__":  
    while True:
        a = get_audio()
        command = audio_to_text(a)
        print(command)
        
        if ACTIVATION_COMMAND in command.lower():
            print("Activated")
            play_sound("I'm listening to you")
            
            note = get_audio()
            note = audio_to_text(note)
            
            if note: 
                play_sound(note)    
                
                time= datetime.now().astimezone().isoformat()
                res= create_page(note, time, status="In progress")
                if res.status_code == 200:
                    play_sound("I have noted that for you")
                
