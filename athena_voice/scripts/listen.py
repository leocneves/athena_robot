import random
import time
import pyttsx3
import speech_recognition as sr
import pandas as pd
from dynaconf import settings
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
            recognizer.adjust_for_ambient_noise(source, duration=1)
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
    engine.say(phrase)
    engine.runAndWait()

    isBusy = engine.isBusy()
    print(isBusy)
    # while engine.isBusy():
    #     time.sleep(.1)
    return None

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
    engine = pyttsx3.init()
    voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PT-BR_MARIA_11.0"

    engine.setProperty('voice', voice)
    engine.setProperty('rate', 150)
    engine.setProperty('volume',1.0)


    # Captura frases das configs

    while True:
        # while not recognizedWord(settings.START_WORD):
        #     continue

        resp = recognize_speech_from_mic(recognizer, microphone)

        try:
            respPhrase = (resp["transcription"]).lower()
            print('Escutei: ', respPhrase)
        except:
            continue

        # for k,v in settings.COMANDOS.items():
        #     v.FRASE
        

        if respPhrase == "fechar simulação":
            say("Simulação finalizada!")
            break
        elif respPhrase.lower() == 'carregar simulação lobo ovelha':
            # say(respPhrase)
            # print(resp)
            say("Simulação aberta!")