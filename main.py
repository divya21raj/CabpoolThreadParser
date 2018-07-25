from mailParser import parse
from mailFetcher import getRecentMail

from firebaseInteractions import pushMap

import sys
import os
import email
import time
from threading import Thread, Event

import imaplib2

def parseAndPush(mailMap):
    #write body to data.txt
    with open("data.txt", "w") as text_file:
        text_file.write(mailMap.get('body'))

    parsedMap = parse()

    finalMailMap = dict(mailMap)
    finalMailMap.update(parsedMap)
    finalMailMap.pop('body')

    print finalMailMap
    pushMap(finalMailMap)


# This is the threading object that does all the waiting on 
# the event
class Idler(object):
    def __init__(self, conn):
        self.thread = Thread(target=self.idle)
        self.M = conn
        self.event = Event()
 
    def start(self):
        self.thread.start()
 
    def stop(self):
        # This is a neat trick to make thread end. Took me a 
        # while to figure that one out!
        self.event.set()
 
    def join(self):
        self.thread.join()
 
    def idle(self):
        # Starting an unending loop here
        while True:
            # This is part of the trick to make the loop stop 
            # when the stop() command is given
            if self.event.isSet():
                return
            self.needsync = False
            # A callback method that gets called when a new 
            # email arrives. Very basic, but that's good.
            def callback(args):
                if not self.event.isSet():
                    self.needsync = True
                    self.event.set()
            # Do the actual idle call. This returns immediately, 
            # since it's asynchronous.
            self.M.idle(callback=callback)
            # This waits until the event is set. The event is 
            # set by the callback, when the server 'answers' 
            # the idle call and the callback function gets 
            # called.
            self.event.wait()
            # Because the function sets the needsync variable,
            # this helps escape the loop without doing 
            # anything if the stop() is called. Kinda neat 
            # solution.
            if self.needsync:
                self.event.clear()
                self.dosync()
 
    # The method that gets called when a new email arrives. 
    # Replace it with something better.
    def dosync(self):
        print "Got an event!"
        mailMap = getRecentMail(self.M)

        if mailMap: #i.e is not empty, i.e from MEGA CT
            print "Is Mega!"
            parseAndPush(mailMap)



#MAIN:

# Had to do this stuff in a try-finally, since some testing 
# went a little wrong.....
try:
    # Set the following two lines to your creds and server
    M = imaplib2.IMAP4_SSL("imap.gmail.com")

    M.login(os.environ.get('SNU_USER_ID', ''), os.environ.get('SNU_PWD', ''))

    # We need to get out of the AUTH state, so we just select 
    # the INBOX.
    M.select("INBOX")
    # Start the Idler thread
    idler = Idler(M)
    idler.start()
    
    #exit after 60 minutes
    time.sleep(59*60)

finally:
    # Clean up.
    idler.stop()
    idler.join()
    M.close()

    # This is important!
    M.logout()
