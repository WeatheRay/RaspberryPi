import RPi.GPIO as GPIO
import time
import signal
import sys
import datetime
#set up GPIO using BCM numbering
#GPIO.setmode(GPIO.BCM)
#setup GPIO usimg Board numbering
GPIO.setmode(GPIO.BOARD)
door = None
oldIsOpen = None
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M.%S")

#print(GPIO.RPI_INFO)


#cleanup clean up
#everybody do your share
def cleanup(signal, frame):
	print(door)
	return door
	sys.exit(0)
#signal.signal(signal.SIGINT, cleanup)

def status(oldDoor):
	#orange = 1
	yellow = 7
	#GPIO.setup(orange,GPIO.OUT,initial=0)
	GPIO.setup(yellow,GPIO.IN,pull_up_down = GPIO.PUD_UP)
	isOpen = ""
	oldIsOpen = None


	if 1==1:
		oldIsOpen = isOpen
		isOpen = GPIO.input(yellow)
		global door
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M.%S")
		if (isOpen and (isOpen != oldIsOpen)):
			oldDoor = "Door is Open\nOpened at: "+now
			return oldDoor
		elif (not isOpen and (isOpen != oldIsOpen)):
			oldDoor = "Door is closed\nClosed at: "+now
			return oldDoor
		GPIO.cleanup()

#status(oldDoor)
