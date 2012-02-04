#!/usr/bin/python

import zmsutils

zmsutils.init()
while True:
    noticeobj = zmsutils.receive(block=True)
    zmsutils.sendText(noticeobj)






