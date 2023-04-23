# -*- coding: utf-8 -*-
import random
import time
#import pyttsx3
from gtts import gTTS
import os
import speech_recognition as sr
import pandas as pd
import Levenshtein

r = sr.Recognizer()
print(sr.Microphone.list_microphone_names())
device = input("Device: ")
mic = sr.Microphone(device_index=int(device))


def say(phrase):
    tts = gTTS(text=phrase, lang='pt-br')

# Salva o arquivo de áudio como "audio.mp3"
    tts.save("/home/ubuntu/catkin_ws/src/athena_robot/athena_voice/scripts/audio.mp3")

# Reproduza o arquivo de áudio usando o player padrão do sistema
    os.system("mpg321 /home/ubuntu/catkin_ws/src/athena_robot/athena_voice/scripts/audio.mp3")
    return None

def beep():
    duration = 0.1  # segundos
    freq = 540  # Hz
    volume = 0.3  # reduzido em 50%
    os.system(f"play -q -n synth {duration} sine {freq} vol {volume}")

def callback(recognizer, audio):
    try:
        recognized_text = recognizer.recognize_google(audio, language='pt-BR')
        print('Você disse:', recognized_text)
    except sr.UnknownValueError:
        print('Não foi possível reconhecer a fala')
    except sr.RequestError as e:
        print(f'Não foi possível se conectar com o serviço: {e}')

def on_unknown(recognizer, audio):
    try:
        recognized_text = recognizer.recognize_google(audio, language='pt-BR')
        print('Você disse:', recognized_text)
    except sr.UnknownValueError:
        print('Não foi possível reconhecer a fala')
    except sr.RequestError as e:
        print(f'Não foi possível se conectar com o serviço: {e}')

with mic as source:
    try:
        mWord = False
        mTimeout = 6 # seconds

        while True:
            r.adjust_for_ambient_noise(source, duration = 1)
            # r.non_speaking_duration = 0.5
            # r.dynamic_energy_threshold = True
            # r.dynamic_energy_adjustment_damping = 0.15
            # r.dynamic_energy_ratio = 1.5
            r.energy_threshold = 100 # 300
            r.operation_timeout = None
            # r.phrase_threshold = 3 #0.3
            r.interim_results = True
            # r.background_timeout = 10
            # r.pause_threshold = 0.8

            print("Diga 'atena' para iniciar o reconhecimento de voz.")
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio, language='pt-BR')
                print(text.lower())
                
                if text.lower() in ['atena', 'athena']:
                    print('Keyword detected in the speech.')
                    say('Olá')
                    mWord = True

                elif (text.lower() == 'quem é você') and mWord:
                    # say(respPhrase)
                    # print(resp)
                    say("Sou a robô para atividades domésticas do Leonardo. Muito prazer.")
                    mWord = False


            except Exception as e:
                print('Please speak again.')

    except KeyboardInterrupt:
        print('interrupted!')
