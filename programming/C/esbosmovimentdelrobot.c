#include "include/IO.h"
#include "include/MandoBluetooth.h"

#define MAXANGLE 40

int main()
{
	char valor;
	float alfa=90,beta=0;
	inicialitzaMM24();
	set(22,6200);//encen el transistor
	//base('d');
	printf("UP per aixecar el robot DOWN per agenollar-lo:alfa:%f beta:%f; LiPo: %.2fV \n\n",alfa,beta,EqBat*llegeix(0));
	valor=llegeixMando();
	while(valor!=START)
	{
		printf("UP per aixecar el robot DOWN per agenollar-lo:alfa:%f beta:%f; LiPo: %.2fV \n\n",alfa,beta,EqBat*llegeix(0));
		switch(valor)
		{
			case UP:
				if (beta>0) beta--;
				if (alfa>0) alfa--;
				break;
			case DOWN:
				if (beta<MAXANGLE) beta++;
				if (alfa<MAXANGLE) alfa++;
				break;
			case RIGHT:
				if (alfa>0) alfa--;
				if (beta<MAXANGLE) beta++;
				break;
			case LEFT:
				if (beta>0) beta--;
				if (alfa<MAXANGLE) alfa++;
				break;
		}
		
		//agenolla(alfa,beta);
		set(HE,alfa*Puls180pangle);
		valor=llegeixMando();
	}
	close(fd);
	return 0;
}
