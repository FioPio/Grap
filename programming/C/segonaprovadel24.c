#include "include/IO.h"

typedef enum {FALSE,TRUE} bool;

int main()
{
	int angle=1200,fd;//20 graus;
	Servo servo=CO;
	char valor;
	bool apagat=FALSE;
	inicialitzaMM24(&fd);
	servosoff(fd);
	printf("u per pujar d per baixar, c per canviar de servo i q per sortir\nServo %u a %d,LiPo: %.2fV \n\n",servo,angle,EqBat*llegeix(fd,0));
	scanf("%c",&valor);
	while(valor!='q')
	{
		printf("u per pujar d per baixar, c per canviar de servo i q per sortir\nServo %u a %d,LiPo: %.2fV \n\n",servo,angle,EqBat*llegeix(fd,0));
		switch(valor)
		{
			case 'q':
				close(fd);
				return 0;
				break;
			case 'u':
				if(angle<10000)angle=angle+100;
				break;
			case 'd':
				if(angle>1200)angle=angle-100;
				break;
			case 'c':
				if(servo<PE) servo++;
				servosoff(fd);
				break;
			case 's':
				apagat=!apagat;
				if(apagat)set(fd,servo,0);
		}
		if(!apagat)set(fd,servo,angle);
		scanf("%c",&valor);
	}
	return 0;
}
