#! /bin/sh

BASEDIR=$(dirname $0)
"$BASEDIR/zms.py" &
#add barnowl
athrun barnowl barnowl
#barnowl