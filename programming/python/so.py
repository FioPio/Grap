from subprocess import call
import time
from threading import Thread as fil

T=30
song="out.mp3"
def musica():
	call(["cvlc","%s"%song])
t1=fil(target=musica)
t1.start()
i=0
while i<T:
	time.sleep(1)
	i+=1
	print( i)
call(["killall","-9","vlc"])
