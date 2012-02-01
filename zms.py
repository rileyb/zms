#!/usr/bin/python

import calendar
from datetime import datetime
import os
import smtplib
import time
import zephyr
from zephyr import receive, ZNotice

varDict = {'USERNAME': 'your_user_name', 'PHONE_NUMBER': 'your_number', 'CARRIER_ADDRESS': 'your_carrier_info', 'WAIT_TIME': '180'}

fh = open(os.path.join(os.environ['HOME'],'.zms.conf'))
for line in fh.readlines():
    for key in varDict.keys():
        if line.startswith(key):
            varDict[key] = line.split('=')[1].strip()

USERNAME = varDict['USERNAME'] # Zephyr username/kerberos name, as a string
PHONE_NUMBER = varDict['PHONE_NUMBER'] # Number at which to receive texts, as a string
CARRIER_ADDRESS = varDict['CARRIER_ADDRESS'] # Carrier-specific appendage to texts e-mailed to phone, as a string (e.g. 'egtext.com')
WAIT_TIME = int(varDict['WAIT_TIME']) # How many seconds to wait before user is considered "away."

def findTime2Unix(zTimeStrng):
    splt = zTimeStrng.split()
    wkday = splt[1]
    month = splt[2]
    moday = splt[3]
    hms = splt[4]
    year = splt[5]
    fixedTimeStrng = ' '.join((wkday, month, moday, hms, year))
    return calendar.timegm((time.strptime(fixedTimeStrng,'%a %b %d %H:%M:%S %Y')))
    
# Heurisic 1: Don't send text if you have sent a zephyr in the last WAIT_TIME  minutes.
def online1(username, n):
    status = 'offline'
    # scan /zlog/class
    for clss in os.listdir(os.path.join(os.environ['HOME'],'zlog/class')):
        fh = open(os.path.join(os.environ['HOME'],'zlog/class/',clss),'r')
        lastline = ''
        for line in fh.readlines():
            line.strip()
            if line.startswith('From') and '<' + username + '>' in line:
                logTime = findTime2Unix(lastline)
                if calendar.timegm(time.localtime())-logTime <= n:
                    status = 'online'
                    return status
            lastline = line
        fh.close()
    # scan /zlog/people/all
    fh = open(os.path.join(os.environ['HOME'],'zlog/people/all'),'r')
    lastline = ''
    for line in fh.readlines():
        line.strip()
        if line.startswith('From') and '<' + username + '>' in line:       
            logTime = findTime2Unix(lastline)
            if calendar.timegm(time.localtime())-logTime <= n:
                status = 'online'
                return status
        lastline = line
    fh.close()
    return status

def zephyrtext(username, phonenum, carrier):
    while True:
        zephyr.init()
        zephyr.Subscriptions().add(('messages', 'personal', '%me%'))
        noticeobj = receive(block=True)
        if online1(username, WAIT_TIME) == 'offline':
            server = smtplib.SMTP('outgoing.mit.edu')
            server.sendmail(
                noticeobj.sender,
                [phonenum+'@'+carrier],
                '''From %s
            
%s''' % (noticeobj.sender,noticeobj.fields[1].strip()))
            
            
zephyrtext(USERNAME, PHONE_NUMBER, CARRIER_ADDRESS)    




