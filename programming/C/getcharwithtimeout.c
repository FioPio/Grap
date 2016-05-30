#include <stdio.h>
#include <unistd.h> //per alarm
#include <signal.h> //pel signal
#include <stdlib.h> //per l'exit 

void got_alarm(int sig) {
fprintf(stderr, "Got signal %d\n", sig);
// exit(1);
}

int main() 
{
	alarm(2);//2 segons
	signal(SIGALRM, got_alarm);
	int c = getchar();
	printf("getchar returned %x\n", c);
	return 0;
}
