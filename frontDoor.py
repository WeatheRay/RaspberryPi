#camera tutorial
#https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/

from picamera import PiCamera, Color
from time import sleep
import uploadImageToSlack
import datetime
import RPi.GPIO as GPIO
import os
import subprocess

#outside function so it is not done each time
camera = PiCamera()
yellow=7
GPIO.setmode(GPIO.BOARD)
outFile = ""
def status():
	now = datetime.datetime.now()
	file ='/home/pi/security/open_door/'+now.strftime("%Y-%m-%d_%H.%M.%S")+'.jpg'
	camera.rotation=270
	#max resolution for still
	#camera.resolution = (2592,1944)
	#camera.framerate = 15
	#max resolution for vid
	#camera.resolution = (1920,1080)

	#min resolution is 64 x 64

	#camera.brightness = 50  1-100
	#camera.brightness = 50 #1-100

	#camera.annotate_text = "hello world"
	#camera.annitate_text_size = 32 #6-160
	#camera.annotate_foregroud = Color('pink') #????
	#camera.annotate_background = Color('green')

	#transparent view of camera
	#camera.start_preview(alpha=200)

	camera.start_preview()

	#picture
	sleep(3)
	camera.capture(file)

	camera.stop_preview()
	uploadImageToSlack.uploadImage(file)

	#take several pictures
	#for i in range(5):
	#	sleep(5)
	#	camera.capture('/home/pi/Desktop/image%s.jpg' %i)
def videoStart():
	#record video
	#view with omxplayer in terminal
	now = datetime.datetime.now()
	global file 
	file='/home/pi/security/open_door/'+now.strftime("%Y-%m-%d_%H.%M.%S")+'.h264'
	camera.rotation=270
#	file = 'test.h264'
	global outFile 
	outFile ='/home/pi/security/open_door/'+now.strftime("%Y-%m-%d_%H.%M.%S")+'.mp4'
#	outFile='test.mp4'
	#record for 10 sec
	open = True
	count = 0	
	GPIO.setup(yellow,GPIO.IN,pull_up_down = GPIO.PUD_UP)
	if (GPIO.input(yellow)):
		camera.start_recording(file)
		return 1

#		while(GPIO.input(yellow)):
#			print(ok)
	#camera.stop_recording()

def videoStop():
	camera.stop_recording()
	camera.stop_preview()
	sleep(3)
	global file
	global outFile
	try:
		convert(file, outFile)
	except subprocess.CalledProcessError as e:
		print('oops')
	#call the script to upload what you just snapped
#	print(output)

def convert(file,outFile):
	command = "MP4Box -add {} {}.mp4".format(file, os.path.splitext(outFile)[0])
	try:
		output = subprocess.check_output(command, stderr = subprocess.STDOUT,shell=True)
	except subprocess.CalledProcessError as e:
		print("FAIL:\ncmd:{}\noutput:{}".format(e.cmd,e.output))
	uploadImageToSlack.uploadImage(outFile)
	
def video():
	now = datetime.datetime.now()
	file='/home/pi/security/open_door/'+now.strftime("%Y-%m-%d_%H.%M.%S")+'.mjpeg'
	camera.start_recording(file)
	sleep(10)
	camera.stop_recording()
	camera.stop_preview()
	uploadImageToSlack.uploadImage(file)


#video()
