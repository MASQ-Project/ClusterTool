#!/bin/bash
TITLE=$1
shift 1

### DOCKER SHELL ENHANCEMENTS
if [ "$SHELL" = '/bin/bash' ]
then
    case $TERM in
         xterm*|rxvt*)
	    echo -ne "\033]0;${TITLE}\007"
         ;;
    esac
fi

echo running $@ ...

$@
