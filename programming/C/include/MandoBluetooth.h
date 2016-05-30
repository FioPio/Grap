/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 *                                                                     *
 *       Bluetoot control using a snake byte device                    *
 *                                                                     *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * This header defines all the necessary files to realize what you need*
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 * @author Ferriol Pey Comas         03/05/2016    @version 1.0        *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

//KEYPAD:
#define UP    'A'
#define DOWN  'B'
#define RIGHT 'C'
#define LEFT  'D'

//BOTONS:
#define X	    'm'
#define Y	    'i'
#define B	    'k'
#define A	    'j'
#define R1	    'p'
#define R2	    'z'
#define R3	    'l'
#define L1	    'q'
#define L2	    'x'
#define L3	    'o'
#define SELECT  'r'
#define START   'y'


//retorna un caracter corresponent a la tecla pulsada
char llegeixMando();
