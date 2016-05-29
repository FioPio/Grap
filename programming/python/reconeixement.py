# python3 putada
# -*- coding: utf-8 -*-
import speech_recognition as sr
from time import sleep as delay
from subprocess import call
import subprocess
import RPi.GPIO as GPIO
LED=21
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED,GPIO.OUT)
GPIO.output(LED,False)

r = sr.Recognizer()
temps=4
delay(3)
call('clear')
delay(2)
GPIO.output(LED,True)
print("\33[38;2;0;0;255;48;2;100;100;100mGraban\x1B[0m")
delay(.3)
call(['arecord','-D','plughw:1','--duration=4','-f','cd','-vv','lect.wav'],stdout=subprocess.PIPE)
GPIO.output(LED,False)
print ("\33[38;2;0;0;255;48;2;100;100;100mGravacio complerta\x1B[0m")
call(['sox','lect.wav','-c','1','lectura.wav'],stdout=subprocess.PIPE)
with sr.WavFile("lectura.wav") as source: # fa servir el microfon per defecte
	audio = r.record(source) #comença a grabar fins al duration en segons
try:
    reconegut=r.recognize(audio)
    print("Has dit " + reconegut) #reconeix fen servir reconeixement de Google
    call(['sh','/home/pi/programes/bash/TTS.sh','you have said: %s'%reconegut])
except IndexError:           # no hi ha conexio
    print("No hi ha connexió a internet")
except LookupError:   # no s'enten
    print("No s'ha entes l'audio")
GPIO.cleanup()
