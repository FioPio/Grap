#!/usr/bin/python2
# -*- encoding: utf-8 -*-
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
    
def llegeix():
    a=getch()
    if ord(a)==27:
        a=getch()
        a=getch()
        return a
    else:
        return a

#c=llegeix()

#while c!= START:
#    print c
#    c=llegeix()
