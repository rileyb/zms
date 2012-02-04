#!/usr/bin/python

import calendar
from datetime import datetime
import os
import time
import zmsutils

varDict = {'USERNAME': 'your_username', 'WAIT_TIME': '180'}
fh = open(os.path.join(os.environ['HOME'],'.zms.conf'))
for line in fh.readlines():
    for key in varDict.keys():
        if line.startswith(key):
            varDict[key] = line.split('=')[1].strip()

USERNAME = varDict['USERNAME']
WAIT_TIME = varDict['WAIT_TIME']

def findTime2Unix(zTimeStrng):
    splt = zTimeStrng.split()
    wkday = splt[1]
    month = splt[2]
    moday = splt[3]
    hms = splt[4]
    year = splt[5]
    fixedTimeStrng = ' '.join((wkday, month, moday, hms, year))
    return calendar.timegm((time.strptime(fixedTimeStrng,'%a %b %d %H:%M:%S %Y')))
    
def onlinep(username, waittime):
    status = 'offline'
    # fh2 = open('/mit/rileyb/Projects/zms/errors','w')
    # fh2.write('got to onlinep\n')
    # fh2.close()
    # scan /zlog/class
    for clss in os.listdir(os.path.join(os.environ['HOME'],'zlog/class')):
        fh = open(os.path.join(os.environ['HOME'],'zlog/class/',clss),'r')
        lastline = ''
        for line in fh.readlines():
            line.strip()
            if line.startswith('From') and '<' + username + '>' in line:
                logTime = findTime2Unix(lastline)
                if calendar.timegm(time.localtime())-logTime <= waittime:
                    # fh2 = open('/mit/rileyb/Projects/zms/errors','a')
                    # fh2.write(str(waittime)+'\n')
                    # fh2.write(str(calendar.timegm(time.localtime())-logTime)+'\n')
                    # fh2.close()
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
            if calendar.timegm(time.localtime())-logTime <= waittime:
                # fh2 = open('/mit/rileyb/Projects/zms/errors','a')
                # fh2.write(str(waittime)+'\n')
                # fh2.write(str(calendar.timegm(time.localtime())-logTime)+'\n')
                # fh2.close()
                status = 'online'
                return status
        lastline = line
    fh.close()
    return status

def zephyrtext():
    zmsutils.init()
    global USERNAME
    global WAIT_TIME
    while True:
        noticeobj = zmsutils.receive(block=True)
        if onlinep(USERNAME, int(WAIT_TIME)) == 'offline':
            zmsutils.sendText(noticeobj)
 # else:
 #            print'online'
 #        #     # fh2 = open('/mit/rileyb/Projects/zms/errors','a')
 #        #     # fh2.write('online\n')
        #     # fh2.close()


zephyrtext()





