#include "include/IO.h"
//                          CA(1)  CO(2)  ZD(3)  ZE(4)  BD(5)  BE(6)  HD(7)  HE(8)  CD(9) CE(10) AD(11) AE(12) FD(13) FE(14) GD(15) GE(16) TD(17) TE(18) PD(19) PE(20)  
unsigned short MAXVAL[] = {     0, 10000,  9920,  8000,  9664, 10176, 10048, 10048,     0,     0,     0,     0, 10048,  9395,  9999,  9999,  9835,  9692,  7647,  7321};
unsigned short MINVAL[] = {     0,  3968,  4000,  1408,  2662,  2952,  1664,  1664,     0,     0,     0,     0,  2880,  2816,  6224,  5776,  5368,  5246,  4720,  4179};
unsigned short BDVAL[]  = {     0,  4984,  7100,  4514,  3600,  9004,  4608,  7177,  6778,  6372,  5750,  6995,  4090,  8200,  9959,  9959,  8519,  6728,  6313,  5691};
unsigned short BVAL[]   = {     0,  4984,  7100,  4514,  3600,  9004,  4608,  7177,  6778,  6372,  5750,  6995,  4090,  8200,  9959,  9959,  8519,  6728,  6313,  5691};
unsigned short POS[20];

int fd;

int inicialitzaMM24()
{
  fd = open("/dev/ttyACM0", O_RDWR | O_NOCTTY);
  if (fd == -1)  return 1;
  struct termios options;
  tcgetattr(fd, &options);
  options.c_iflag &= ~(INLCR | IGNCR | ICRNL | IXON | IXOFF);
  options.c_oflag &= ~(ONLCR | OCRNL);
  options.c_lflag &= ~(ECHO | ECHONL | ICANON | ISIG | IEXTEN);
  tcsetattr(fd, TCSANOW, &options);
  return 0;
}

int llegeix(unsigned char canal)//10 bits
{
  unsigned char command[] = {0x90,canal};
  if(write(fd, command, sizeof(command)) == -1)
  {
    perror("Error Llegin");
    return -1;
  }
  unsigned char response[2];
  if(read(fd,response,2) != 2)
  {
    perror("Error Llegint");
    return -1;
  }
  return response[0] + (int)256.75*response[1];
}

int set(unsigned char canal, unsigned short senyal)
{
  unsigned char command[] = {0x84, canal, senyal & 0x7F, senyal >> 7 & 0x7F};
  if (write(fd, command, sizeof(command)) == -1)
  {
    perror("error writing");
    return -1;
  }
  POS[canal]=senyal;
  return 0;
}

void base(char c)
{
  int i;
  for(i=1;i<=sizeof(BDVAL)/sizeof(unsigned short);i++) //sizeof(BVAL)/sizeof(unsigned short)= valors al vector
  {
    if(c=='d')   set(i,BDVAL[i]);
    else set(i,BVAL[i-1]);
    system("sleep 0.001");
  } 
}

void agenolla(float a,float b)
{
  float gamma=a+b;
  //femurs girant alpha graus
  set(FE,BDVAL[FE]-a*Puls180pangle);
  set(FD,BDVAL[FD]+a*Puls180pangle);
  //genolls girant gamma graus
  set(GE,BDVAL[GE]-gamma*Puls180pangle);
  set(GD,BDVAL[GD]-gamma*Puls180pangle);
  //tormells girant beta graus
  set(TE,BDVAL[TE]+b*Puls180pangle);
  set(TD,BDVAL[TD]-b*Puls180pangle);
}
