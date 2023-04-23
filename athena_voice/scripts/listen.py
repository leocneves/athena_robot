# -*- coding: utf-8 -*-
import random
import time
#import pyttsx3
from gtts import gTTS
import os
import speech_recognition as sr
import pandas as pd
import Levenshtein

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    print('Gravando ...')
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.6)
            recognizer.energy_threshold = 100
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
    except:
        print('Timeout excedido ... ')
        response = {
            "success": False,
            "error": "Microphone timeout",
            "transcription": None
        }
        return response
    print('Gravado!')

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio, language="pt-BR")
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    print(response)
    return response

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

def recognizedWord(word):
    resp = recognize_speech_from_mic(recognizer, microphone)
    if (not resp['error']) and (resp["transcription"] == word):
        return True
    else:
        return False

def comparaFrases(fra, frb):
    return True if Levenshtein.ratio(fra, frb) >= settings.CORTE_LEVEN else False

if __name__ == "__main__":
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    # sr.Microphone.list_microphone_names()
    microphone = sr.Microphone(device_index=1)


    # Captura frases das configs
    mWord = False

    while True:
        # while not recognizedWord(settings.START_WORD):
        #     continue

        resp = recognize_speech_from_mic(recognizer, microphone)

        try:
            respPhrase = (resp["transcription"]).lower()
            print('Escutei: ', respPhrase)
        except:
            continue

        if respPhrase == "atena":
            say("Olá!")
            beep()
            mWord = True
            #break
        elif (respPhrase.lower() == 'que dia é hoje') and mWord:
            # say(respPhrase)
            # print(resp)
            say("Hoje é dia 7 de abril, aniversário do menino egito. Parabéns egito!")
            mWord = False
        elif (respPhrase.lower() == 'quem é você') and mWord:
            # say(respPhrase)
            # print(resp)
            say("Sou a robô para atividades domésticas do Leonardo. Muito prazer.")
            mWord = False

