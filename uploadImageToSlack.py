import requests
import sys


def uploadImage(file):

        files = {
            'file': (file, open(file, 'rb')),
            'channels': (None, 'the-den'),
            'token': (None, 'SLACKTOEKN'),
        }

        response = requests.post('https://slack.com/api/files.upload', files=files)

if len(sys.argv) >1:
        file = sys.argv[1]
        uploadImage(file)



#files = {
#    'file': ('/home/pi/Desktop/image.jpg', open('/home/pi/Desktop/image.jpg', 'rb')),
#    'channels': (None, 'the-den'),
#    'token': (None, 'SLACKTOKEN'),
#}

#response = requests.post('https://slack.com/api/files.upload', files=files)
