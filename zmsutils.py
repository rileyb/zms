import os
import smtplib
import zephyr
from zephyr import receive, ZNotice

PHONE_NUMBER = 'None'
CARRIER_ADDRESS = 'None'
noticeobj = 'None'

def getVars():
    varDict = {'PHONE_NUMBER': 'your_number', 'CARRIER_ADDRESS': 'your_carrier_info'}
    fh = open(os.path.join(os.environ['HOME'],'.zmsconf'))
    for line in fh.readlines():
        for key in varDict.keys():
            if line.startswith(key):
                varDict[key] = line.split('=')[1].strip()
    global PHONE_NUMBER
    global CARRIER_ADDRESS
    PHONE_NUMBER = varDict['PHONE_NUMBER'] 
    CARRIER_ADDRESS = varDict['CARRIER_ADDRESS'] 

def init():
    getVars()
    zephyr.init()
    zephyr.Subscriptions().add(('messages', 'personal', '%me%'))

def sendText(noticeobj, mailServer='outgoing.mit.edu'):
    server = smtplib.SMTP(mailServer)
    global PHONE_NUMBER
    global CARRIER_ADDRESS
    server.sendmail(
        noticeobj.sender,
        [PHONE_NUMBER+'@'+CARRIER_ADDRESS],
        '''From %s

%s''' % (noticeobj.sender, noticeobj.fields[1].strip()))
