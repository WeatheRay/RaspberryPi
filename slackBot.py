#!/usr/bin/python

import os
import time
import re
import frontDoor
from slackclient import SlackClient
import magDoor
import signal
import sys
import log
import datetime
import RPi.GPIO as GPIO

#this will get the pi's IP to post into slack
f = os.popen('ifconfig wlan0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
ip = f.read()
ipPrint = 0
yellow = 7
isOpen = None
oldIsOpen = None
recording = 0
# instantiate Slack client
#export SLACK_BOT_TOKEN='SLACKTOKEN'
slack_client = SlackClient('SLACKTOKEN')
slack_client.api_call
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = .5 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "/do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def cleanup(signal, frame):
        sys.exit(0)
signal.signal(signal.SIGINT, cleanup)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    if command == "/help" or "/h":
        response = "/update : picture of the living room and last change\n/status : last change"
    if command == "/update":
        frontDoor.status()
        response = log.read()
    if command== "/status":
        response = log.read()

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("---WatchWolf Online---")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            GPIO.setup(yellow,GPIO.IN,pull_up_down = GPIO.PUD_UP)
            oldIsOpen = isOpen
            isOpen = GPIO.input(yellow)
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M.%S")
            if(ipPrint == 0):
                slack_client.api_call(
                        "chat.postMessage",
                        channel="CASRL3GTC",
                        text="My IP is : " + ip
                )
                ipPrint =1;
            if (isOpen and (isOpen != oldIsOpen)):
                log.write("Front door opened",now)
                slack_client.api_call(
                        "chat.postMessage",
                        channel="CASRL3GTC",
                        text=now+"\tFront door opened"
                )
                recording = frontDoor.videoStart()


            elif (not isOpen and (isOpen != oldIsOpen)):
                log.write("Front door closed",now)
                slack_client.api_call(
                       "chat.postMessage",
                        channel="CASRL3GTC",
                        text=now+"\tFront door closed"
                )
                if recording:
                        frontDoor.videoStop()


            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

