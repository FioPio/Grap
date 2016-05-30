#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <termios.h>
#define eqbat  6.87/671.00

int maestroGetPosition(int fd, unsigned char channel)//10 bits
{
  unsigned char command[] = {0x90, channel};
  if(write(fd, command, sizeof(command)) == -1)
  {
    perror("error writing");
    return -1;
  }
 
  unsigned char response[2];
  if(read(fd,response,2) != 2)
  {
    perror("error reading");
    return -1;
  }
 
  return response[0] + (int)256.75*response[1];
}
 
// Sets the target of a Maestro channel.
// See the "Serial Servo Commands" section of the user's guide.
// The units of 'target' are quarter-microseconds.
int maestroSetTarget(int fd, unsigned char channel, unsigned short target)
{
  unsigned char command[] = {0x84, channel, target & 0x7F, target >> 7 & 0x7F};
  if (write(fd, command, sizeof(command)) == -1)
  {
    perror("error writing");
    return -1;
  }
  return 0;
}
 
int main()
{
  // Open the Maestro's virtual COM port.
  const char * device = "/dev/ttyACM0";  // Linux
  int fd = open(device, O_RDWR | O_NOCTTY);
  if (fd == -1)
  {
    perror(device);
    return 1;
  }
   struct termios options;
  tcgetattr(fd, &options);
  options.c_iflag &= ~(INLCR | IGNCR | ICRNL | IXON | IXOFF);
  options.c_oflag &= ~(ONLCR | OCRNL);
  options.c_lflag &= ~(ECHO | ECHONL | ICANON | ISIG | IEXTEN);
  tcsetattr(fd, TCSANOW, &options);
 
  //int position = maestroGetPosition(fd, 0);
  //printf("Voltatge: %fV amb valor %d.\n", position*eqbat,position);
  
  //int target=(position < 6000) ? 7000 : 5000; //(condicio) ? false : true;
 // printf("Setting target to %d (%d us).\n", target, target/4);
  maestroSetTarget(fd, 5, 10000);// per a les sortides digitals si és igual o major a  1500 picosegons = high! per tant 1500*4 i per servos va de 0 a 10000, que correspon de 0 a 2500 *4
 
  close(fd);
  return 0;
}
