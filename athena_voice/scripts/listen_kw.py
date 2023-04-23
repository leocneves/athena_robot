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
mic = sr.Microphone(device_index=1)


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
        while True:
            r.adjust_for_ambient_noise(source)
            print("Diga 'atena' para iniciar o reconhecimento de voz.")
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio)
                print(text.lower())
                if text.lower() == 'atena':
                    print('Keyword detected in the speech.')
            except Exception as e:
                print('Please speak again.')

    except KeyboardInterrupt:
        print('interrupted!')

    # # Configura o objeto para reconhecer a palavra-chave
    # keyword_recognizer = sr.Recognizer()
    # keyword_recognizer.set_keyphrase('atena')
    # # keyword_recognizer.add_keyword('atenção', 0.5)  # adiciona outra palavra-chave
    # keyword_recognizer.set_callback(callback)

    # # Reconhece a palavra-chave
    # try:
    #     keyword_recognizer.recognize_google(audio)
    # except sr.UnknownValueError:
    #     print('Não foi possível reconhecer a fala')

    # # Configura o objeto para reconhecer frases não incluindo a palavra-chave
    # r.set_keyword_recognizer(keyword_recognizer)
    # r.pause_threshold = 0.5
    # r.non_speaking_duration = 0.5
    # r.dynamic_energy_threshold = True
    # r.dynamic_energy_adjustment_damping = 0.15
    # r.dynamic_energy_ratio = 1.5
    # r.energy_threshold = 300
    # r.operation_timeout = None
    # r.phrase_threshold = 0.3
    # r.interim_results = True
    # r.background_timeout = 10
    # r.pause_threshold = 0.8
    # r.set_unknown_callback(on_unknown)

    # # Começa a gravar novamente e reconhece frases sem a palavra-chave
    # print("Agora você pode falar qualquer coisa.")
    # audio = r.listen(source)
    # try:
    #     recognized_text = r.recognize_google(audio, language='pt-BR')
    #     print('Você disse:', recognized_text)
    # except sr.UnknownValueError:
    #     print('Não foi possível reconhecer a fala')
    # except sr.RequestError as e:
    #     print(f'Não foi possível se conectar com o serviço: {e}')