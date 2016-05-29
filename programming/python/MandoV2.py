#!/usr/bin/python2
# -*- encoding: utf-8 -*-
import signal
import time

#KEYPAD:
UP    = 'A'
DOWN  = 'B'
RIGHT = 'C'
LEFT  = 'D'

#BOTONS:
X	   = 'm'
Y	   = 'i'
B	   = 'k'
A	   = 'j'
R1	   = 'p'
R2	   = 'z'
R3	   = 'l'
L1	   = 'q'
L2	   = 'x'
L3	   = 'o'
SELECT = 'r'
START  = 'y'

# Defineix la  funcio del trhead
def timeout():
	raise Exception('Temps fora')
   
def getch(): #https://rosettacode.org/wiki/Keyboard_input/Keypress_check#Python el dia 25 de maig de 2016
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
    
def llegeix(t):
    try:
        if t!=0.00:
            signal.signal(signal.SIGALRM, timeout)
            signal.alarm(t)
        a=getch()
    except:
        a='0'
    if t!=0.00:
        signal.alarm(0)
    if ord(a)==27:
        a=getch()
        a=getch()
        return a
    else:
        return a

k=llegeix(1)
while k!=START:
    print 'apretat ',k
    k=llegeix(2)
