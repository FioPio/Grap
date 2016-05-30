#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

char tecla()
{
	char c;
	system("/bin/stty raw");//intro sola
	c=getchar();
	if(c==27)//fletxa te una estructura de ESC + '[' + A|B|C|D
	{
		c=getchar();
		c=getchar();
	}
	system("/bin/stty cooked");//treu lu de intro sola o la lia
	if(c=='A')	   c='U';//UP
	else if(c=='B')c='D';//DOWN
	else if(c=='C')c='R';//RIGHT
	else if(c=='D')c='L';//LEFT
	return c;
}

int main()
{
	char apretada=tecla();
	while(apretada!='Q')
	{
		printf("ha retornat %c\n",apretada);
		apretada=tecla();
	}
}
