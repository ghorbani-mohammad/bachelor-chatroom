import _thread
import time

def print_time(threadName,delay):
    count=0
    while count<5:
        time.sleep(delay)
        count+=1
        print(""+threadName+": "+time.ctime(time.time()))
try:
    _thread.start_new_thread(print_time,("Thread-1",2,))
    _thread.start_new_thread(print_time,("Thread-2",4,))
except:
    print("Unable To Start New Thread")

while 1:
    pass