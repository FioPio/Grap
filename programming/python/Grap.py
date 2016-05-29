#!/usr/bin/python2
# -*- encoding: utf-8 -*-
#############################################################################################################################
#                                                                                                                           #
#                                                           GRAP                                                            # 
#                                                                                                                           #
#############################################################################################################################
#                                                            @Fio                                                           #
#############################################################################################################################
import time
from MMC24 import Device
from subprocess import call
import cv2
import Mando

#********************************************************Dispositius**********************************************************

mm   = Device()  # MiniMaestro
#*********************************************************constants***********************************************************

batmin = 6.15          # bat minima en Volts
eqbat  = 7.34/198.00   # equivalencia voltatge de la lipo
UD     = 20            # ull dret
UE     = 21            # ull esquerre
BO     = 16            # boca
T      = 18            # transistor
BI     =  batmin/eqbat # bateria minima en bits (al voltant de 180)
a180   = 180.00/2550   # equivalencia angles servos 180º
a270   = 270.00/2550   # equivalencia angles servos 270º
#Mando:
#keypad:
UP    = 'A'
DOWN  = 'B'
RIGHT = 'C'
LEFT  = 'D'
#botons:
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
#servos
CA=1;CO=2;ZD=3;ZE=4;BD=5;BE=6;HD=7;HE=8;CD=9;CE=10;AD=11;AE=12;FD=13;FE=14;GD=15;GE=16;TD=17;TE=18;PD=19;PE=20
SPA=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]     # servos posicio actual
s=[1,2,3,4,5,6,7,8]
#          CA(1)  CO(2)  ZD(3)  ZE(4)  BD(5)  BE(6)  HD(7)  HE(8)  CD(9) CE(10) AD(11) AE(12) FD(13) FE(14) GD(15) GE(16) TD(17) TE(18) PD(19) PE(20) 
MAXVAL = [     0, 10000,  9920,  8000,  9664, 10176, 10048, 10048, 10000,10000,  10000, 10000, 10048,  9395,  9999,  9999,  9835,  9692,  7647,  7321]
MINVAL = [     0,  3968,  4000,  1408,  2662,  2952,  1664,  1664,     0,     0,     0,     0,  2880,  2816,  6224,  5776,  5368,  5246,  4720,  4179]
BDVAL  = [     0,  4984,  7100,  4514,  3600,  9004,  4608,  7177,  6778,  6372,  5750,  6995,  4300,  8000,  9959,  9899,  8519,  6699,  6313,  5691]
BVAL   = [     0,  4984,  7100,  4514,  3600,  9004,  4608,  7177,  6778,  6372,  5750,  6995,  5556,  6860,  8324,  8292,  7616,  7540,  6313,  5691]
BGVAL  = [     0,  4984,  7100,  4514,  3600,  9004,  4608,  7177,  6778,  6372,  5750,  6995,  7168,  5404,  6236,  6108,  6560,  8524,  6313,  5691]
#******************************************************accions i fucions****************************************************** 

def servo(a,n):
	if MAXVAL[a-1]/4>=n and MINVAL[a-1]/4<=n:# si està en el rang del servo
		mm.set_target(a,n)
		SPA[a-1]=n  #apunta la posició actual
	else:
		print '%s no pot arribar a %d'%(a,n)

def basedret():
	print 'servos a base dret'
	for a in range(1,21):
		servo(a,BDVAL[a-1]/4)

def basegenolls():
	print 'servos a base genolls'
	for a in range(1,21):
		servo(a,BGVAL[a-1]/4)

def base():
	print 'servos a base'
	for a in range(1,21):
		servo(a,BVAL[a-1]/4)
			
def llbat():  
	print
	BatL=0
	print '\x1B[37;1mBateria:\x1B[m'
	BatL = mm.get_position(0)# pin de la bateria
	print ("Lipo     : "+ "%.2f" %(BatL*eqbat) + " Volts\x1B[m")
	print
	if BatL< BI:  
		print('\x1B[31;40m'+'********************************************'+'\x1B[m')
		print('\x1B[31;40m'+'**************LIPO SENSE BATERIA************'+'\x1B[m')
		print('\x1B[31;40m'+'********************************************'+'\x1B[m')
		print 
	return BatL

def agenolla(t,c,b): #base a c50
	print 'Agenollant'
	#         FE,   FD,   GE,   GD,   TE,  TD
	PGS = [  794.0,  874.0, 1115.0, 1135.0,  588.0,  626.0]#764.0, 844.0, 1115.0, 1135.0,  538.0,  576.0
	steps=100
	Puls180pangle=2500/(180*4) # un quart d'angle
	#femurs girant alpha graus
	if c>85:
		c=85
	for i in range(b,c+1):
		servo(FE,(BDVAL[FE-1]/4)-int((PGS[0]/steps)*i))
		servo(FD,(BDVAL[FD-1]/4)+int((PGS[1]/steps)*i))
		#genolls girant gamma graus
		servo(GE,(BDVAL[GE-1]/4)-int((PGS[2]/steps)*i))
		servo(GD,(BDVAL[GD-1]/4)-int((PGS[3]/steps)*i))
		#tormells girant beta graus
		servo(TE,(BDVAL[TE-1]/4)+int((PGS[4]/steps)*i))
		servo(TD,(BDVAL[TD-1]/4)-int((PGS[5]/steps)*i))
		time.sleep(t/steps)
	if c>84:
		basegenolls()
		
def desagenolla(t,c,b): #base a c50
	print 'desagenollant'
	#         FE,   FD,   GE,   GD,   TE,  TD
	PGS = [  794.0,  874.0, 1115.0, 1135.0,  588.0,  626.0]#764.0, 844.0, 1115.0, 1135.0,  538.0,  576.0
	steps=100
	Puls180pangle=2500/(180*4) # un quart d'angle
	#femurs girant alpha graus
	if c>85:
		c=85
	for j in range(b,c+1):
		i=86-j
		servo(FE,(BDVAL[FE-1]/4)-int((PGS[0]/steps)*i))
		servo(FD,(BDVAL[FD-1]/4)+int((PGS[1]/steps)*i))
		#genolls girant gamma graus
		servo(GE,(BDVAL[GE-1]/4)-int((PGS[2]/steps)*i))
		servo(GD,(BDVAL[GD-1]/4)-int((PGS[3]/steps)*i))
		#tormells girant beta graus
		servo(TE,(BDVAL[TE-1]/4)+int((PGS[4]/steps)*i))
		servo(TD,(BDVAL[TD-1]/4)-int((PGS[5]/steps)*i))
		time.sleep(t/steps)

###############################################DESPLAÇAMENT######################

def giraE():
	print 'girant a la esquerra'
	#posa el pes al peu dret
	for i in range(0,10):
		servo(PE,BVAL[PE-1]/4-12*i)
		servo(AE,BVAL[AE-1]/4-12*i)
		servo(PD,BVAL[PD-1]/4-12*i)
		servo(AD,BVAL[AD-1]/4-12*i)
		time.sleep(0.04)
	#aixeca cama esquerre
	for i in range(0,10):
		servo(TE,BVAL[TE-1]/4+4*i)
		servo(FE,BVAL[FE-1]/4-4*i)
		servo(GE,BVAL[GE-1]/4-8*i)
		time.sleep(0.04)
	#gira cintura
	for i in range(0,10):
		servo(CD,BVAL[CD-1]/4+15*i)
		servo(CE,BVAL[CE-1]/4-15*i)
		time.sleep(0.04)
	#baixa cama esquerre:
	for j in range(0,10):
		i=9-j
		servo(TE,BVAL[TE-1]/4+4*i)
		servo(FE,BVAL[FE-1]/4-4*i)
		servo(GE,BVAL[GE-1]/4-8*i)
		time.sleep(0.04)
	#torna el pes al centre:
	for j in range(0,10):
		i=9-j
		servo(PE,BVAL[PE-1]/4-12*i)
		servo(AE,BVAL[AE-1]/4-12*i)
		servo(PD,BVAL[PD-1]/4-12*i)
		servo(AD,BVAL[AD-1]/4-12*i)
		time.sleep(0.04)
	#i ara recupera el mateix a l'altre peu:
	#posa el pes al peu esquerre
	for i in range(0,10):
		servo(PE,BVAL[PE-1]/4+12*i)
		servo(AE,BVAL[AE-1]/4+12*i)
		servo(PD,BVAL[PD-1]/4+12*i)
		servo(AD,BVAL[AD-1]/4+12*i)
		time.sleep(0.04)
	#gira cintura
	for j in range(0,10):
		i=9-j
		servo(CD,BVAL[CD-1]/4+15*i)
		servo(CE,BVAL[CE-1]/4-15*i)
		time.sleep(0.04)
	#recupera el pes:
	for j in range(0,10):
		i=9-j
		servo(PE,BVAL[PE-1]/4+12*i)
		servo(AE,BVAL[AE-1]/4+12*i)
		servo(PD,BVAL[PD-1]/4+12*i)
		servo(AD,BVAL[AD-1]/4+12*i)
		time.sleep(0.04)

def giraD():
	print 'giran a la dreta'
	#posa el pes al peu esquerre
	for i in range(0,10):
		servo(PE,BVAL[PE-1]/4+12*i)
		servo(AE,BVAL[AE-1]/4+12*i)
		servo(PD,BVAL[PD-1]/4+12*i)
		servo(AD,BVAL[AD-1]/4+12*i)
		time.sleep(0.04)
	#aixeca cama dreta 
	for i in range(0,10):
		servo(TD,BVAL[TD-1]/4-4*i)
		servo(FD,BVAL[FD-1]/4+4*i)
		servo(GD,BVAL[GD-1]/4-8*i)
		time.sleep(0.04)
	#gira cintura
	for i in range(0,10):
		servo(CD,BVAL[CD-1]/4+15*i)
		servo(CE,BVAL[CE-1]/4-15*i)
		time.sleep(0.04)
	#baixa cama dreta:
	for j in range(0,10):
		i=9-j
		servo(TD,BVAL[TD-1]/4-4*i)
		servo(FD,BVAL[FD-1]/4+4*i)
		servo(GD,BVAL[GD-1]/4-8*i)
		time.sleep(0.04)
	#torna el pes al centre:
	for j in range(0,10):
		i=9-j
		servo(PE,BVAL[PE-1]/4+12*i)
		servo(AE,BVAL[AE-1]/4+12*i)
		servo(PD,BVAL[PD-1]/4+12*i)
		servo(AD,BVAL[AD-1]/4+12*i)
		time.sleep(0.04)
	#i ara recupera el mateix a l'altre peu:###########################
	#posa el pes al peu dret
	for i in range(0,10):
		servo(PE,BVAL[PE-1]/4-12*i)
		servo(AE,BVAL[AE-1]/4-12*i)
		servo(PD,BVAL[PD-1]/4-12*i)
		servo(AD,BVAL[AD-1]/4-12*i)
		time.sleep(0.04)
	#aixeca cama esquerre
	for i in range(0,10):
		servo(TE,BVAL[TE-1]/4+4*i)
		servo(FE,BVAL[FE-1]/4-4*i)
		servo(GE,BVAL[GE-1]/4-8*i)
		time.sleep(0.04)
	#gira cintura
	for j in range(0,10):
		i=9-j
		servo(CD,BVAL[CD-1]/4+15*i)
		servo(CE,BVAL[CE-1]/4-15*i)
		time.sleep(0.04)
	for j in range(0,10):
		i=9-j
		servo(TE,BVAL[TE-1]/4+4*i)
		servo(FE,BVAL[FE-1]/4-4*i)
		servo(GE,BVAL[GE-1]/4-8*i)
		time.sleep(0.04)
	#recupera el pes:
	for j in range(0,10):
		i=9-j
		servo(PE,BVAL[PE-1]/4-12*i)
		servo(AE,BVAL[AE-1]/4-12*i)
		servo(PD,BVAL[PD-1]/4-12*i)
		servo(AD,BVAL[AD-1]/4-12*i)
		time.sleep(0.04)

def camina():
	print 'Caminant'
	#posa el pes al peu dret
	for i in range(0,10):
		servo(PE,BVAL[PE-1]/4-12*i)
		servo(AE,BVAL[AE-1]/4-12*i)
		servo(PD,BVAL[PD-1]/4-12*i)
		servo(AD,BVAL[AD-1]/4-12*i)
		time.sleep(0.04)
	#aixeca cama esquerre
	for i in range(0,10):
		servo(TE,BVAL[TE-1]/4+4*i)
		servo(FE,BVAL[FE-1]/4-4*i)
		servo(GE,BVAL[GE-1]/4-8*i)
		time.sleep(0.04)
	#gira cintura
	for i in range(0,10):
		servo(CD,BVAL[CD-1]/4-15*i) #+
		servo(CE,BVAL[CE-1]/4-15*i)
		time.sleep(0.04)
	#baixa cama esquerre:
	for j in range(0,10):
		i=9-j
		servo(TE,BVAL[TE-1]/4+4*i)
		servo(FE,BVAL[FE-1]/4-4*i)
		servo(GE,BVAL[GE-1]/4-8*i)
		time.sleep(0.04)
	#torna el pes al centre:
	for j in range(0,10):
		i=9-j
		servo(PE,BVAL[PE-1]/4-12*i)
		servo(AE,BVAL[AE-1]/4-12*i)
		servo(PD,BVAL[PD-1]/4-12*i)
		servo(AD,BVAL[AD-1]/4-12*i)
		time.sleep(0.04)
	#i ara recupera el mateix a l'altre peu:
	#posa el pes al peu esquerre
	for i in range(0,10):
		servo(PE,BVAL[PE-1]/4+12*i)
		servo(AE,BVAL[AE-1]/4+12*i)
		servo(PD,BVAL[PD-1]/4+12*i)
		servo(AD,BVAL[AD-1]/4+12*i)
		time.sleep(0.04)
	#gira cintura
	for j in range(0,10):
		i=9-j
		servo(CD,BVAL[CD-1]/4-15*i)
		servo(CE,BVAL[CE-1]/4-15*i)
		time.sleep(0.04)
	#recupera el pes:
	for j in range(0,10):
		i=9-j
		servo(PE,BVAL[PE-1]/4+12*i)
		servo(AE,BVAL[AE-1]/4+12*i)
		servo(PD,BVAL[PD-1]/4+12*i)
		servo(AD,BVAL[AD-1]/4+12*i)
		time.sleep(0.04)
		
	base()
'''
POSTURETI#########################################################################
'''
def saluda():
	print 'saludan'
	for i in range(0,101):
		servo(HE,BVAL[HE-1]/4-3*i)
		servo(HD,BVAL[HD-1]/4-3*i)
		time.sleep(0.005)
	for i in range(0,101):
		servo(ZE,BVAL[ZE-1]/4+7*i)
		servo(ZD,BVAL[ZD-1]/4-6*i)
		time.sleep(0.005)
		
	for i in range(0,101):
		servo(FE,BVAL[FE-1]/4-2*i)
		servo(FD,BVAL[FD-1]/4+2*i)
		time.sleep(0.005)
		
	time.sleep(1.5)
	for i in range(0,101):
		j=100-i
		servo(FE,BVAL[FE-1]/4-2*j)
		servo(FD,BVAL[FD-1]/4+2*j)
		time.sleep(0.005)
		
	for i in range(0,101):
		j=100-i
		servo(ZE,BVAL[ZE-1]/4+7*j)
		servo(ZD,BVAL[ZD-1]/4-6*j)
		time.sleep(0.005)
	for i in range(0,101):
		j=100-i
		servo(HE,BVAL[HE-1]/4-3*j)
		servo(HD,BVAL[HD-1]/4-3*j)
		time.sleep(0.005)
	base()
	
'''
##########################################################################################################################

							Programa principal

##########################################################################################################################
'''
print 'activant servos'
mm.set_target(22,1550)#encenservos
time.sleep(0.2)
if llbat()<BI:
	quit()
print 'aixecantse'
time.sleep(0.2)
basegenolls()
time.sleep(1)
desagenolla(1.176,50,0)#2.0 perfecte
base()
llbat()
#print 'saludan: '
#saluda()
#time.sleep(3)
#desagenolla(2-1.176,100,50)#s'aixeca fins a dret
#print 'agenollat: '
#llbat()
#giraD()
#time.sleep(1)
#giraE()
#time.sleep(1)
#saluda()
#time.sleep(1.2)
#agenolla(1.176,86,36) #s'agenolla desde base
camina()
time.sleep(1.2)
agenolla(1.176,86,36) #s'agenolla desde base
'''
key=Mando.llegeix()

while key!=START:
	elif key==UP:
		i=0
	elif key==DOWN:
		i=1
	elif key==RIGHT:
		i=2
	elif key==LEFT:
		i=3
	elif key==L1:
		giraE()
	elif key==L2:
		i=5
	elif key==L3:
		i=6
	elif key==R3:
		saluda()
	elif key==R1:
		giraD()
	elif key==R2:
		i=7
	elif key==X:
		i=8
	elif key==A:
		i=9
	key=Mando.llegeix()
agenolla(1.176,86,36)# s'agenolla
'''
