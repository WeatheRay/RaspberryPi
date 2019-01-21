def write(data,time):
	file = open('/home/pi/security/log.log','a+')
	file.write(time+"\t"+data+"\n")
	file.close()
def read():
	file = open('/home/pi/security/log.log','a+')
	x=""
	for line in file:
		x=line
	return x	
        file.close()        
	
#print(read())
#file.close()
