extern "C" //li diu que son llibreries de C
{
	#include "include/IO.h"
}

int main()
{
	Servo servo;
	servo=CO;
	int fd;
	inicialitzaMM24(&fd);//en c: "/dev/ttyACM0",&fd);
	llegeix(fd,servo);
	return 0;
}
