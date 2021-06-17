import os
import playsound
import speech_recognition as sr
import os
import playsound
import speech_recognition as sr
import time
import sys
import ctypes
import wikipedia
import datetime
import json
import re
import webbrowser
import smtplib
import requests
import urllib
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
from youtube_search import YoutubeSearch
import serial #Serial imported for Serial communication
import time #Required to use delay functions
import pyttsx3
#nndanwndsanwnd

wikipedia.set_lang('vi')
language = 'vi'
path = ChromeDriverManager().install()
try: 
    ArduinoSerial = serial.Serial('com3',9600) #Create Serial port object called arduinoSerialData
    time.sleep(2) #wait for 2 secounds for the communication to get established
    print("Connected...")
except:
    print("Fail on connect...!!!!")


def speak(text):
    print("Bot: {}".format(text))
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", False)
    os.remove("sound.mp3")

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Tôi: ", end='')
        audio = r.listen(source, phrase_time_limit=2)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text
        except:
            print("...")
            return 0

def stop():
    speak("Hẹn gặp lại bạn sau!")

def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 2:
            print("...")
    time.sleep(2)
    
    return 0

def play_song():
    speak('Xin mời bạn chọn tên bài hát')
    mysong = get_text()
    while True:
        result = YoutubeSearch(mysong, max_results=10).to_dict()
        if result:
            break
    url = 'https://www.youtube.com' + result[0]['url_suffix']
    webbrowser.open(url)
    speak("Bài hát bạn yêu cầu đã được mở.")

    


    


    

def assistant():
    
    
#     name = get_text()
    name = "Sơn"
    if name:
        speak("Chào bạn {}".format(name))
        time.sleep(2)
        
        while True:
            text = get_text()
            if not text:
                print("not text")
            elif "dừng" in text or "tạm biệt" in text or "chào robot" in text or "ngủ thôi" in text:
                stop()
                break
            elif "bật" in text and "khách" in text:
                print("đã bật khách")
            elif "bật" in text and "ngủ" in text:
                print("đã bật ngủ")
            elif "bật" in text and "vệ" in text:
                print("đã bật vệ sinh")
            elif "tắt" in text and "khách" in text:
                print("đã tắt khách")
            elif "tắt" in text and "ngủ" in text:
                print("đã tắt ngủ")
            elif "tắt" in text and "vệ" in text:
                print("đã tắt vệ sinh")
            
           
          
            
            elif "chơi nhạc" in text:
                play_song()
            
            else:
                speak("Bạn cần Bot giúp gì ạ?")

assistant()

