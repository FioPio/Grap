#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <termios.h>

#define EqBat  6.87/671.00
#define Puls180pangle (2500*4)/180 //pulsos 4 cicles per picosegon entre 180º
#define Puls270pangle (2500*4)/270 //pulsos 4 cicles per picosegon entre 180º

typedef enum {CA=1,CO=2,ZD=3,ZE=4,BD=5,BE=6,HD=7,HE=8,CD=9,CE=10,AD=11,AE=12,FD=13,FE=14,GD=15,GE=16,TD=17,TE=18,PD=19,PE=20}Servo;
typedef enum {FALSE,TRUE} bool;

extern unsigned short MAXVAL[];
extern unsigned short MINVAL[];
extern unsigned short BVAL[];
extern unsigned short BDVAL[];
extern unsigned short POS[];
extern int fd;
/*Inicia la placa*/
int inicialitzaMM24();//char* dispositiu,int*fd);
/* serveix per llegir entrades de la MM24 amb resolució de 10 bits*/
int llegeix(unsigned char canal);
/* serveix per definir una sortida de la MM24 (per servos va de 0 a 10000, que correspon de 0 a 2500x4)*/
int set(unsigned char canal, unsigned short senyal);
//Posa tots els servos a Base;
void base(char c);
//juga amb els genolls:
void agenolla(float a,float b);
