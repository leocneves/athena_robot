# -*- coding: utf-8 -*-

import random
import time
#import pyttsx3
from gtts import gTTS
import os
import speech_recognition as sr
import pandas as pd
import Levenshtein
import openai

# Ros
import rospy
import yaml
# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

rospy.init_node('movebase_client_py')
# Define global variables
r = sr.Recognizer()
print(sr.Microphone.list_microphone_names())
device = input("Device: ")
mic = sr.Microphone(device_index=int(device))
openai.api_key = ""
model_engine = "text-davinci-003"

#####
checkpoints = yaml.safe_load(open('../../athena_nav/param/checkpoints.yaml', 'r'))


def goTo(cp):

   # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
 
   # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()

   # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
   # Move 0.5 meters forward along the x axis of the "map" coordinate frame 
    goal.target_pose.pose.position.x = checkpoints[cp]['position']['x']
    goal.target_pose.pose.position.y = checkpoints[cp]['position']['y']
   # No rotation of the mobile base frame w.r.t. map frame
    goal.target_pose.pose.orientation.z = checkpoints[cp]['orientation']['z']
    goal.target_pose.pose.orientation.w = checkpoints[cp]['orientation']['w']

   # Sends the goal to the action server.
    client.send_goal(goal)
   # Waits for the server to finish performing the action.
    wait = client.wait_for_result()
   # If the result doesn't arrive, assume the Server is not available
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
    # Result of executing the action
        return client.get_result()  
    
#####

def say(phrase):
    tts = gTTS(text=phrase, lang='pt-br')

# Salva o arquivo de áudio como "audio.mp3"
    tts.save("/home/athena/catkin_ws/src/athena_robot/athena_voice/scripts/audio.mp3")

# Reproduza o arquivo de áudio usando o player padrão do sistema
    os.system("mpg321 /home/athena/catkin_ws/src/athena_robot/athena_voice/scripts/audio.mp3")
    return None

def beep():
    duration = 0.1  # segundos
    freq = 540  # Hz
    volume = 0.3  # reduzido em 50%
    # os.system(f"play -q -n synth {duration} sine {freq} vol {volume}")
    os.system("ogg123 /usr/share/sounds/freedesktop/stereo/bell.oga")

def beepComplete():
    duration = 0.1  # segundos
    freq = 540  # Hz
    volume = 0.3  # reduzido em 50%
    # os.system(f"play -q -n synth {duration} sine {freq} vol {volume}")
    os.system("ogg123 /usr/share/sounds/freedesktop/stereo/complete.oga")


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
            r.adjust_for_ambient_noise(source, duration = 2)
            r.non_speaking_duration = 1.5
            # r.dynamic_energy_threshold = True
            # r.dynamic_energy_adjustment_damping = 0.15
            # r.dynamic_energy_ratio = 1.5
            # r.energy_threshold = 70 # 300
            # r.operation_timeout = None
            # r.phrase_threshold = 0.7 #0.3
            # r.interim_results = True
            # r.background_timeout = 5
            r.pause_threshold = 2.0

            print("Diga 'atena' para iniciar o reconhecimento de voz.")
            audio = r.listen(source, timeout=10, phrase_time_limit=4)

            try:
                text = r.recognize_google(audio, language='pt-BR')
                print(text.lower())

                if text.lower() in ['atena', 'athena']:
                    print('Keyword detected in the speech.')
                    say('Olá')
                    beep()
                    mWord = True

                elif (text.lower() == 'quem é você') and mWord:
                    # say(respPhrase)
                    # print(resp)
                    say("Sou a robô para atividades domésticas do Leonardo. Muito prazer.")
                    mWord = False
###############

                elif (text.lower() in ['vá para a mesa da sala', 'va para a mesa da sala']) and mWord:
                    say("Você gostaria que eu vá até a mesa da sala?")
                    beep()

                    while True:
                        print("CONFIRAMAÇÃO")
                        audio = r.listen(source, timeout=10, phrase_time_limit=2)
                        
                        try:
                            text = r.recognize_google(audio, language='pt-BR').lower()
                            print(text)

                            if text == 'sim':
                                say("OK, estou indo!")
                                goTo('mesa_sala')
                                break
                            elif text in ['não', 'nao']:
                                say("OK!")
                                break

                        except Exception as e:
                            print('Erro: ', e)
                            continue


                    mWord = False

                elif (text.lower() in ['vá para o escritório', 'va para o escritorio']) and mWord:
                    say("Você gostaria que eu vá até o escritório?")
                    beep()

                    while True:
                        print("CONFIRAMAÇÃO")
                        audio = r.listen(source, timeout=10, phrase_time_limit=2)
                        
                        try:
                            text = r.recognize_google(audio, language='pt-BR').lower()
                            print(text)

                            if text == 'sim':
                                say("OK, estou indo!")
                                goTo('escritorio')
                                break
                            elif text in ['não', 'nao']:
                                say("OK!")
                                break

                        except Exception as e:
                            print('Erro: ', e)
                            continue


                    mWord = False

###############

                elif (text) and mWord:
                    completion = openai.Completion.create(
                        engine=model_engine,
                        prompt=text,
                        max_tokens=1024,
                        n=1,
                        stop=None,
                        temperature=0.8,
                    )

                    say(completion['choices'][0]["text"])


            except Exception as e:
                print('Please speak again.', e)

    except KeyboardInterrupt:
        print('interrupted!')
