#! /bin/sh

BASEDIR=$(dirname $0)
"$BASEDIR/zms.py" &
athrun barnowl barnowl
