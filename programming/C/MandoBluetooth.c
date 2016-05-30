/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 *                                                                     *
 *       Bluetoot control using a snake byte device                    *
 *                                                                     *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * This file defines all the necessary functions to do what you need   *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * @author Ferriol Pey Comas         03/05/2016    @version 1.0        *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
 
#include "include/MandoBluetooth.h"

char llegeixMando()
{
	char c;
	system("/bin/stty raw");//intro sola despres de cada pulsació
	c=getchar();
	if(c==27)//una tecla de fletxa te una estructura de ESC + '[' + A|B|C|D
	{
		c=getchar();//'['
		c=getchar();// A|B|C|D
	}
	system("/bin/stty cooked");//treu l'intro sola
	if(c=='A')	   c=UP;
	else if(c=='B')c=DOWN;
	else if(c=='C')c=RIGHT;
	else if(c=='D')c=LEFT;
	return c;
}
